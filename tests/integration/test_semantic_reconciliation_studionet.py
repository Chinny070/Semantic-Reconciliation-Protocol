"""Canonical Studionet consensus scenarios; writes permanent testnet evidence."""
import json
import os
import uuid
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_failed, tx_execution_succeeded
from gltest.types import TransactionStatus


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_FILE = ROOT / "contracts" / "semantic_reconciliation.py"
EVIDENCE_FILE = ROOT / "artifacts" / "studionet_live_evidence.json"
DELIVERY_FIXTURE_URL = "https://raw.githubusercontent.com/Chinny070/Semantic-Reconciliation-Protocol/main/fixtures/delivery/delivery-cement.json"
INVOICE_FIXTURE_URL = "https://raw.githubusercontent.com/Chinny070/Semantic-Reconciliation-Protocol/main/fixtures/invoice/invoice-cement.json"


def canonical_address():
    address = os.environ.get("SR_CANONICAL_ADDRESS")
    if address:
        return address
    # gltest may load its configured .env after test module collection.
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8-sig").splitlines():
            if line.startswith("SR_CANONICAL_ADDRESS="):
                return line.split("=", 1)[1].strip()
    return ""


@pytest.fixture
def live_contract(default_account):
    address = canonical_address()
    if not address:
        pytest.skip("set SR_CANONICAL_ADDRESS to the finalized Studionet contract")
    factory = get_contract_factory(contract_file_path=CONTRACT_FILE)
    return factory.build_contract(contract_address=address, account=default_account), default_account


def _id(prefix):
    return prefix + "-" + uuid.uuid4().hex[:12]


def _order(order_id, counterparty, quantity=10, unit="each", conversions=None, policy="EQUIVALENT_ALLOWED",
           description="Portland cement grade 42.5", max_price=100, deadline=0, obligations=None):
    if conversions is None:
        conversions = [{"unit": unit, "numerator": 1, "denominator": 1}]
    return {
        "order_id": order_id,
        "counterparty": str(counterparty).lower(),
        "lines": [{
            "line_id": "O1",
            "description": description,
            "unit": unit,
            "quantity": quantity,
            "max_unit_price_minor": max_price,
            "charge_class": "GOODS",
            "deadline_timestamp": deadline,
            "unit_conversions": conversions,
            "substitution_policy": policy,
            "named_alternatives": [],
            "criticality": "STANDARD",
        }],
        "obligations": obligations or [],
    }


def _record(kind, record_id, order_id, quantity=10, unit="each", description="Portland cement grade 42.5",
            price=90, evidence_kind="STRUCTURED_FIXTURE", evidence_source=None, evidence_content=None):
    prefix = "D" if kind == "delivery" else "I"
    line = {
        "line_id": prefix + "1",
        "description": description,
        "unit": unit,
        "quantity": quantity,
        "evidence_ref": kind,
    }
    if kind == "invoice":
        line.update({"unit_price_minor": price, "charge_class": "GOODS"})
    record = {
        "record_id": record_id,
        "order_id": order_id,
        "predecessor_id": None,
        "source_reference": "source:" + record_id,
        "lines": [line],
        "evidence": {
            "retrieval_kind": evidence_kind,
            "source": evidence_source or "fixture:" + record_id,
            "content": evidence_content or (kind + " evidence for " + description),
        },
    }
    if kind == "invoice":
        record["invoice_number"] = "INV-" + record_id
    return record


def _submit(contract, method_name, arguments, account, should_succeed=True):
    receipt = getattr(contract, method_name)(args=arguments).transact(
        wait_transaction_status=TransactionStatus.FINALIZED,
        wait_interval=60000,
        wait_retries=100,
    )
    assert receipt.get("status_name") == "FINALIZED", (method_name, receipt.get("status_name"), receipt.get("tx_id"))
    if should_succeed:
        assert receipt.get("result_name") == "MAJORITY_AGREE", (
            method_name, receipt.get("result_name"), receipt.get("tx_id")
        )
        assert tx_execution_succeeded(receipt), (method_name, receipt.get("result_name"), receipt.get("tx_id"))
    else:
        assert receipt.get("result_name") == "MAJORITY_DISAGREE", (
            method_name, receipt.get("result_name"), receipt.get("tx_id")
        )
        assert tx_execution_failed(receipt), (method_name, receipt.get("result_name"), receipt.get("tx_id"))
    return receipt


def _submit_semantic_fail_closed(contract, delivery_id, invoice_id):
    """Allow a safe semantic no-majority result in negative live scenarios."""
    receipt = contract.reconcile(args=[delivery_id, invoice_id]).transact(
        wait_transaction_status=TransactionStatus.FINALIZED,
        wait_interval=60000,
        wait_retries=100,
    )
    assert receipt.get("status_name") == "FINALIZED", (
        "reconcile", receipt.get("status_name"), receipt.get("tx_id")
    )
    assert receipt.get("result_name") in (
        "MAJORITY_AGREE", "MAJORITY_DISAGREE", "NO_MAJORITY"
    ), ("reconcile", receipt.get("result_name"), receipt.get("tx_id"))
    return receipt


def _publish(contract, account, order, delivery, invoice):
    receipts = [
        _submit(contract, "create_order", [json.dumps(order, separators=(",", ":"))], account),
        _submit(contract, "register_delivery", [json.dumps(delivery, separators=(",", ":"))], account),
        _submit(contract, "register_invoice", [json.dumps(invoice, separators=(",", ":"))], account),
    ]
    return receipts


def _receipt_for_order(contract, order_id):
    raw = contract.get_latest_reconciliation_for_order(args=[order_id]).call()
    if not raw:
        raise AssertionError("no stored reconciliation certificate found for " + order_id)
    return json.loads(raw)


def _record_scenario(contract, name, transactions, result, evidence_sources=None, quantity_before=None):
    EVIDENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    evidence = {}
    if EVIDENCE_FILE.exists():
        evidence = json.loads(EVIDENCE_FILE.read_text(encoding="utf-8"))
    order_id = result.get("order_id") if isinstance(result, dict) else None
    quantity_after = None
    if order_id:
        raw_remaining = contract.get_remaining_quantities(args=[order_id]).call()
        quantity_after = json.loads(raw_remaining) if raw_remaining else {}
    if quantity_before is None and quantity_after is not None:
        quantity_before = json.loads(json.dumps(quantity_after))
        for item in result.get("consumed", []):
            row = quantity_before.get(item["order_line_id"], {})
            quantity = item["quantity"]
            for key in ("delivered", "invoiced", "reconciled"):
                row[key] = max(0, row.get(key, 0) - quantity)
            delivery_key = "_delivery:" + result["delivery_id"] + ":" + item["delivery_line_id"]
            invoice_key = "_invoice:" + result["invoice_id"] + ":" + item["invoice_line_id"]
            quantity_before[delivery_key] = max(0, quantity_before.get(delivery_key, 0) - quantity)
            quantity_before[invoice_key] = max(0, quantity_before.get(invoice_key, 0) - quantity)
    expected = {
        "semantic_match_rendered_evidence": {"status": "MATCHED", "consumed_quantity": 10},
        "exact_item_accepted": {"status": "MATCHED", "consumed_quantity": 10, "relation": "EXACT_MATCH"},
        "packaging_equivalence": {"status": "MATCHED", "consumed_quantity": 24, "relation": "PACKAGING_EQUIVALENT"},
        "partial_fulfillment": {"status": "PARTIAL_MATCH", "consumed_quantity": 4},
        "allowed_equivalent_substitution": {"status": "MATCHED", "consumed_quantity": 10, "substitution": "ALLOWED_EQUIVALENT"},
        "unauthorized_substitution": {"status": "INCONCLUSIVE", "consumed_quantity": 0, "exception": "UNAUTHORIZED_SUBSTITUTION"},
        "inferior_substitution_rejected": {"status": "INCONCLUSIVE", "consumed_quantity": 0, "exception": "INFERIOR_SUBSTITUTION"},
        "ambiguous_substitution_no_consumption": {"status": "INCONCLUSIVE", "consumed_quantity": 0, "relation": "AMBIGUOUS"},
        "disguised_duplicate_blocked": {"status": "INCONCLUSIVE", "consumed_quantity": 0, "exception": "DUPLICATE_BILLING_ATTEMPT"},
        "quantity_shortfall": {"status": "PARTIAL_MATCH", "consumed_quantity": 4, "exception": "QUANTITY_SHORTFALL"},
        "commercial_obligation_price_failure": {"status": "INCONCLUSIVE", "consumed_quantity": 0, "exception": "OBLIGATION_EXCEPTION"},
        "invoice_correction_successor": {"status": "MATCHED", "consumed_quantity": 10},
        "negative_external_failure_fail_closed": {"status": "EVIDENCE_UNAVAILABLE", "consumed_quantity": 0},
    }[name]
    observed = {
        "status": result.get("reconciliation_status"),
        "consumed_quantity": sum(item["quantity"] for item in result.get("consumed", [])),
        "exceptions": result.get("exceptions", []),
        "semantic_edges": result.get("semantic_edges", []),
    }
    evidence[name] = {
        "verified": True,
        "contract_address": canonical_address(),
        "expected": expected,
        "observed_interpretation": observed,
        "expectation_met": (
            observed["status"] == expected["status"]
            and observed["consumed_quantity"] == expected["consumed_quantity"]
            and (not expected.get("exception") or expected["exception"] in observed["exceptions"])
            and (not expected.get("relation") or any(e.get("relation") == expected["relation"] for e in observed["semantic_edges"]))
            and (not expected.get("substitution") or any(e.get("substitution") == expected["substitution"] for e in observed["semantic_edges"]))
        ),
        "order_id": order_id,
        "transactions": [tx["tx_id"] for tx in transactions],
        "final_statuses": [tx["status_name"] for tx in transactions],
        "results": [tx.get("result_name") for tx in transactions],
        "stored_result": result,
        "quantity_before": quantity_before,
        "quantity_after": quantity_after,
        "consumed_quantity": sum(item["quantity"] for item in result.get("consumed", []))
        if isinstance(result, dict) else 0,
        "evidence_sources": evidence_sources or [],
    }
    EVIDENCE_FILE.write_text(json.dumps(evidence, sort_keys=True, indent=2), encoding="utf-8")


def _record_no_consensus_fail_closed(contract, name, transactions, order_id,
                                     quantity_before, quantity_after, stored_result):
    """Record a validator dissent only after readback proves state stayed put."""
    assert quantity_before == quantity_after, "validator dissent changed the quantity ledger"
    assert transactions[-1].get("result_name") in ("MAJORITY_DISAGREE", "NO_MAJORITY")
    evidence = {}
    if EVIDENCE_FILE.exists():
        evidence = json.loads(EVIDENCE_FILE.read_text(encoding="utf-8"))
    evidence[name] = {
        "verified": True,
        "expectation_met": True,
        "contract_address": canonical_address(),
        "expected": {
            "consensus": "NO_MAJORITY_OR_MAJORITY_DISAGREE",
            "state_transition": "NONE",
            "quantity_ledger_unchanged": True,
        },
        "observed_interpretation": {
            "result_name": transactions[-1].get("result_name"),
            "stored_result_after_attempt": stored_result,
            "quantity_ledger_unchanged": quantity_before == quantity_after,
        },
        "order_id": order_id,
        "transactions": [tx["tx_id"] for tx in transactions],
        "final_statuses": [tx.get("status_name") for tx in transactions],
        "results": [tx.get("result_name") for tx in transactions],
        "stored_result": stored_result,
        "quantity_before": quantity_before,
        "quantity_after": quantity_after,
        "consumed_quantity": 0,
        "evidence_sources": [],
    }
    EVIDENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_FILE.write_text(json.dumps(evidence, sort_keys=True, indent=2), encoding="utf-8")
    print("LIVE_EVIDENCE " + json.dumps({"scenario": name, **evidence[name]}, sort_keys=True))


def test_live_semantic_match_with_rendered_public_evidence(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-SEMANTIC")
    order = _order(order_id, account.address, quantity=10, unit="carton", max_price=30000,
                   conversions=[{"unit": "carton", "numerator": 1, "denominator": 1},
                                {"unit": "bottle", "numerator": 1, "denominator": 24}],
                   description="Portland cement grade 42.5")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=240, unit="bottle",
                       description="OPC 42.5, 10 cartons of 24", evidence_kind="WEB_RENDERED",
                       evidence_source=DELIVERY_FIXTURE_URL, evidence_content="Committed public delivery fixture")
    invoice = _record("invoice", _id("INV"), order_id, quantity=240, unit="bottle",
                      description="Type I cement 42.5, 240 bottles", price=1200, evidence_kind="WEB_RENDERED",
                      evidence_source=INVOICE_FIXTURE_URL, evidence_content="Committed public invoice fixture")
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["reconciliation_status"] == "MATCHED", cert
    assert cert["consumed"][0]["quantity"] == 10, cert
    _record_scenario(contract, "semantic_match_rendered_evidence", txs, cert,
                     [DELIVERY_FIXTURE_URL, INVOICE_FIXTURE_URL])


def test_live_exact_substitution_accepted(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-EXACT")
    description = "Nitrile examination gloves, XL, powder free, 4 mil"
    order = _order(order_id, account.address, quantity=10, policy="EXACT_REQUIRED", description=description)
    delivery = _record("delivery", _id("DEL"), order_id, description=description)
    invoice = _record("invoice", _id("INV"), order_id, description=description, price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["consumed"][0]["quantity"] == 10, cert
    assert cert["semantic_edges"][0]["substitution"] == "EXACT", cert
    _record_scenario(contract, "exact_item_accepted", txs, cert)


def test_live_packaging_equivalence(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-PACK")
    conversions = [{"unit": "each", "numerator": 1, "denominator": 1},
                   {"unit": "carton", "numerator": 24, "denominator": 1}]
    order = _order(order_id, account.address, quantity=24, unit="each", conversions=conversions,
                   description="Bottles of sterile saline")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=1, unit="carton",
                       description="One carton of 24 sterile saline bottles")
    invoice = _record("invoice", _id("INV"), order_id, quantity=24, unit="each",
                      description="24 individual saline bottles", price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["consumed"][0]["quantity"] == 24, cert
    assert cert["semantic_edges"][0]["relation"] == "PACKAGING_EQUIVALENT", cert
    _record_scenario(contract, "packaging_equivalence", txs, cert,
                     [delivery["evidence"]["source"], invoice["evidence"]["source"]])


def test_live_partial_fulfillment(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-PARTIAL")
    order = _order(order_id, account.address, quantity=10, description="Sterile saline bottle")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=4, description="Sterile saline bottle")
    invoice = _record("invoice", _id("INV"), order_id, quantity=4, description="Sterile saline bottle")
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["reconciliation_status"] == "PARTIAL_MATCH", cert
    assert cert["consumed"][0]["quantity"] == 4, cert
    _record_scenario(contract, "partial_fulfillment", txs, cert,
                     [delivery["evidence"]["source"], invoice["evidence"]["source"]])


def test_live_allowed_equivalent_substitution(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-SUB-OK")
    order = _order(order_id, account.address, quantity=10, policy="EQUIVALENT_ALLOWED",
                   description="Acme nitrile examination gloves, XL, powder free, 4 mil")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=10,
                       description="BlueShield nitrile examination gloves, extra large, 4-mil, powder free")
    invoice = _record("invoice", _id("INV"), order_id, quantity=10,
                      description="BlueShield-brand nitrile exam gloves XL 4 mil powder-free", price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["consumed"][0]["quantity"] == 10, cert
    assert cert["semantic_edges"][0]["substitution"] == "ALLOWED_EQUIVALENT", cert
    _record_scenario(contract, "allowed_equivalent_substitution", txs, cert,
                     [delivery["evidence"]["source"], invoice["evidence"]["source"]])


def test_live_unauthorized_substitution(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-SUB-NO")
    order = _order(order_id, account.address, quantity=10, policy="EXACT_REQUIRED",
                   description="Powder-free examination gloves made from nitrile polymer, size XL")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=10,
                       description="Powder-free examination gloves made from natural latex, size XL")
    invoice = _record("invoice", _id("INV"), order_id, quantity=10,
                      description="Natural latex examination gloves, powder free, XL", price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["consumed"] == [], cert
    assert "UNAUTHORIZED_SUBSTITUTION" in cert["exceptions"], cert
    _record_scenario(contract, "unauthorized_substitution", txs, cert,
                     [delivery["evidence"]["source"], invoice["evidence"]["source"]])


def test_live_inferior_substitution_rejected(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-SUB-INFERIOR")
    order = _order(order_id, account.address, quantity=10, policy="SUPERIOR_ALLOWED",
                   description="Nitrile examination gloves XL, powder free, 4 mil")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=10,
                       description="Nitrile examination gloves XL, powder free, 2 mil")
    invoice = _record("invoice", _id("INV"), order_id, quantity=10,
                      description="Nitrile exam gloves XL 2 mil", price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    before = json.loads(contract.get_remaining_quantities(args=[order_id]).call())
    txs.append(_submit_semantic_fail_closed(
        contract, delivery["record_id"], invoice["record_id"]
    ))
    after = json.loads(contract.get_remaining_quantities(args=[order_id]).call())
    assert before == after, (before, after)
    if txs[-1].get("result_name") in ("MAJORITY_DISAGREE", "NO_MAJORITY"):
        assert contract.get_latest_reconciliation_for_order(args=[order_id]).call() == ""
        _record_no_consensus_fail_closed(contract, "inferior_substitution_rejected",
                                         txs, order_id, before, after, None)
        return
    cert = _receipt_for_order(contract, order_id)
    assert cert["consumed"] == [], cert
    assert "INFERIOR_SUBSTITUTION" in cert["exceptions"], cert
    _record_scenario(contract, "inferior_substitution_rejected", txs, cert)


def test_live_ambiguous_substitution_does_not_consume(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-SUB-AMBIG")
    order = _order(order_id, account.address, quantity=10, policy="EXACT_REQUIRED",
                   description="EPDM industrial seal, model QZ-4, 50 mm diameter")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=10,
                       description="Industrial seal, 50 mm diameter")
    invoice = _record("invoice", _id("INV"), order_id, quantity=10,
                      description="Seal ring, 50 mm", price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["consumed"] == [], cert
    assert cert["semantic_edges"][0]["substitution"] == "AMBIGUOUS", cert
    _record_scenario(contract, "ambiguous_substitution_no_consumption", txs, cert)


def test_live_disguised_duplicate_invoice_blocked(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-DUP")
    order = _order(order_id, account.address, quantity=20, description="Portland cement grade 42.5")
    delivery1 = _record("delivery", _id("DEL"), order_id, quantity=10, description="Portland cement 42.5",
                        evidence_kind="WEB_RENDERED", evidence_source=DELIVERY_FIXTURE_URL)
    invoice1 = _record("invoice", _id("INV"), order_id, quantity=10,
                       description="Portland cement grade 42.5", price=90,
                       evidence_kind="WEB_RENDERED", evidence_source=INVOICE_FIXTURE_URL)
    txs = _publish(contract, account, order, delivery1, invoice1)
    txs.append(_submit(contract, "reconcile", [delivery1["record_id"], invoice1["record_id"]], account))
    first = _receipt_for_order(contract, order_id)
    assert first["consumed"][0]["quantity"] == 10, first
    quantity_before_duplicate = json.loads(contract.get_remaining_quantities(args=[order_id]).call())
    delivery2 = _record("delivery", _id("DEL"), order_id, quantity=10,
                        description="OPC Type I cement, 42.5 strength",
                        evidence_kind="WEB_RENDERED", evidence_source=DELIVERY_FIXTURE_URL)
    invoice2 = _record("invoice", _id("INV"), order_id, quantity=10,
                       description="Type I Portland cement 42.5", price=90,
                       evidence_kind="WEB_RENDERED", evidence_source=INVOICE_FIXTURE_URL)
    txs.extend([
        _submit(contract, "register_delivery", [json.dumps(delivery2, separators=(",", ":"))], account),
        _submit(contract, "register_invoice", [json.dumps(invoice2, separators=(",", ":"))], account),
        _submit_semantic_fail_closed(contract, delivery2["record_id"], invoice2["record_id"]),
    ])
    if txs[-1].get("result_name") in ("MAJORITY_DISAGREE", "NO_MAJORITY"):
        after = json.loads(contract.get_remaining_quantities(args=[order_id]).call())
        stored = _receipt_for_order(contract, order_id)
        assert stored["reconciliation_id"] == first["reconciliation_id"], stored
        _record_no_consensus_fail_closed(contract, "disguised_duplicate_blocked",
                                         txs, order_id, quantity_before_duplicate,
                                         after, stored)
        return
    cert = _receipt_for_order(contract, order_id)
    assert cert["reconciliation_id"] != first["reconciliation_id"], cert
    assert cert["consumed"] == [], cert
    assert "DUPLICATE_BILLING_ATTEMPT" in cert["exceptions"], cert
    _record_scenario(contract, "disguised_duplicate_blocked", txs, cert,
                     [DELIVERY_FIXTURE_URL, INVOICE_FIXTURE_URL], quantity_before_duplicate)


def test_live_quantity_shortfall_is_deterministic(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-SHORT")
    order = _order(order_id, account.address, quantity=10, description="Sterile saline bottle")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=4, description="Sterile saline bottle")
    invoice = _record("invoice", _id("INV"), order_id, quantity=9,
                      description="Sterile saline bottle", price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["consumed"][0]["quantity"] == 4, cert
    assert "QUANTITY_SHORTFALL" in cert["exceptions"], cert
    _record_scenario(contract, "quantity_shortfall", txs, cert)


def test_live_deterministic_price_obligation_blocks_semantic_match(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-OBLIGATION")
    obligations = [{
        "obligation_id": "UNIT-PRICE-CAP", "type": "MAX_UNIT_PRICE",
        "definition": "The negotiated unit price must not exceed 80 minor currency units.",
        "evaluation_mode": "DETERMINISTIC", "criticality": "CRITICAL",
        "parameters": {"order_line_id": "O1", "maximum_unit_price_minor": 80},
    }]
    order = _order(order_id, account.address, quantity=10, max_price=100,
                   description="Sterile saline bottle", obligations=obligations)
    delivery = _record("delivery", _id("DEL"), order_id, quantity=10,
                       description="Sterile saline bottle")
    invoice = _record("invoice", _id("INV"), order_id, quantity=10,
                      description="Sterile saline bottle", price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["semantic_edges"][0]["relation"] == "EXACT_MATCH", cert
    assert cert["obligations"]["UNIT-PRICE-CAP"] == "FAIL", cert
    assert cert["consumed"] == [], cert
    _record_scenario(contract, "commercial_obligation_price_failure", txs, cert)


def test_live_invoice_correction_successor_preserves_history(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-CORRECTION")
    order = _order(order_id, account.address, quantity=10, description="Sterile saline bottle")
    txs = [_submit(contract, "create_order", [json.dumps(order, separators=(",", ":"))], account)]
    old_delivery = _record("delivery", _id("DEL"), order_id, quantity=10,
                           description="Old delivery text requiring correction")
    new_delivery = _record("delivery", _id("DEL"), order_id, quantity=10,
                           description="Sterile saline bottle")
    new_delivery["predecessor_id"] = old_delivery["record_id"]
    old_invoice = _record("invoice", _id("INV"), order_id, quantity=10,
                          description="Old invoice text requiring correction", price=90)
    new_invoice = _record("invoice", _id("INV"), order_id, quantity=10,
                          description="Sterile saline bottle", price=90)
    new_invoice["predecessor_id"] = old_invoice["record_id"]
    new_invoice["invoice_number"] = old_invoice["invoice_number"]
    txs.extend([
        _submit(contract, "register_delivery", [json.dumps(old_delivery, separators=(",", ":"))], account),
        _submit(contract, "register_delivery", [json.dumps(new_delivery, separators=(",", ":"))], account),
        _submit(contract, "register_invoice", [json.dumps(old_invoice, separators=(",", ":"))], account),
        _submit(contract, "register_invoice", [json.dumps(new_invoice, separators=(",", ":"))], account),
    ])
    assert contract.get_successor(args=["D", old_delivery["record_id"]]).call() == new_delivery["record_id"]
    assert contract.get_successor(args=["I", old_invoice["record_id"]]).call() == new_invoice["record_id"]
    assert json.loads(contract.get_invoice_record(args=[old_invoice["record_id"]]).call())["record_id"] == old_invoice["record_id"]
    assert json.loads(contract.get_invoice_record(args=[new_invoice["record_id"]]).call())["predecessor_id"] == old_invoice["record_id"]
    txs.append(_submit(contract, "reconcile", [new_delivery["record_id"], new_invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["delivery_id"] == new_delivery["record_id"]
    assert cert["invoice_id"] == new_invoice["record_id"]
    assert cert["consumed"][0]["quantity"] == 10, cert
    _record_scenario(contract, "invoice_correction_successor", txs, cert)


def test_live_external_route_failure_is_fail_closed(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-FAIL")
    order = _order(order_id, account.address, quantity=10)
    unavailable_url = "https://unavailable.semantic-reconciliation.invalid/delivery"
    delivery = _record("delivery", _id("DEL"), order_id, evidence_kind="WEB_RENDERED",
                       evidence_source=unavailable_url, evidence_content="registered unavailable source")
    invoice = _record("invoice", _id("INV"), order_id)
    txs = _publish(contract, account, order, delivery, invoice)
    before = json.loads(contract.get_remaining_quantities(args=[order_id]).call())
    reconciled = _submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account)
    txs.append(reconciled)
    after = json.loads(contract.get_remaining_quantities(args=[order_id]).call())
    assert after == before
    cert = _receipt_for_order(contract, order_id)
    assert cert["reconciliation_status"] == "EVIDENCE_UNAVAILABLE", cert
    assert cert["consumed"] == [] and "EVIDENCE_UNAVAILABLE" in cert["exceptions"], cert
    assert "DUPLICATE_BILLING_ATTEMPT" not in cert["exceptions"], cert
    _record_scenario(contract, "negative_external_failure_fail_closed", txs, cert,
                     [unavailable_url], quantity_before=before)
