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
           description="Portland cement grade 42.5", max_price=100, deadline=0):
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
        "obligations": [],
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
        wait_interval=20000,
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


def _record_scenario(name, transactions, result):
    EVIDENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    evidence = {}
    if EVIDENCE_FILE.exists():
        evidence = json.loads(EVIDENCE_FILE.read_text(encoding="utf-8"))
    evidence[name] = {
        "verified": True,
        "transactions": [tx["tx_id"] for tx in transactions],
        "final_statuses": [tx["status_name"] for tx in transactions],
        "results": [tx.get("result_name") for tx in transactions],
        "stored_result": result,
    }
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
    _record_scenario("semantic_match_rendered_evidence", txs, cert)


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
    _record_scenario("packaging_equivalence", txs, cert)


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
    _record_scenario("partial_fulfillment", txs, cert)


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
    _record_scenario("allowed_equivalent_substitution", txs, cert)


def test_live_unauthorized_substitution(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-SUB-NO")
    order = _order(order_id, account.address, quantity=10, policy="EXACT_REQUIRED",
                   description="Nitrile examination gloves XL")
    delivery = _record("delivery", _id("DEL"), order_id, quantity=10, description="Latex examination gloves XL")
    invoice = _record("invoice", _id("INV"), order_id, quantity=10,
                      description="Latex gloves size XL", price=90)
    txs = _publish(contract, account, order, delivery, invoice)
    txs.append(_submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account))
    cert = _receipt_for_order(contract, order_id)
    assert cert["consumed"] == [], cert
    assert "UNAUTHORIZED_SUBSTITUTION" in cert["exceptions"], cert
    _record_scenario("unauthorized_substitution", txs, cert)


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
    delivery2 = _record("delivery", _id("DEL"), order_id, quantity=10,
                        description="OPC Type I cement, 42.5 strength",
                        evidence_kind="WEB_RENDERED", evidence_source=DELIVERY_FIXTURE_URL)
    invoice2 = _record("invoice", _id("INV"), order_id, quantity=10,
                       description="Type I Portland cement 42.5", price=90,
                       evidence_kind="WEB_RENDERED", evidence_source=INVOICE_FIXTURE_URL)
    txs.extend([
        _submit(contract, "register_delivery", [json.dumps(delivery2, separators=(",", ":"))], account),
        _submit(contract, "register_invoice", [json.dumps(invoice2, separators=(",", ":"))], account),
        _submit(contract, "reconcile", [delivery2["record_id"], invoice2["record_id"]], account),
    ])
    cert = _receipt_for_order(contract, order_id)
    assert cert["reconciliation_id"] != first["reconciliation_id"], cert
    assert cert["consumed"] == [], cert
    assert "DUPLICATE_BILLING_ATTEMPT" in cert["exceptions"], cert
    _record_scenario("disguised_duplicate_blocked", txs, cert)


def test_live_external_route_failure_is_fail_closed(live_contract):
    contract, account = live_contract
    order_id = _id("LIVE-FAIL")
    order = _order(order_id, account.address, quantity=10)
    delivery = _record("delivery", _id("DEL"), order_id, evidence_kind="WEB_RENDERED",
                       evidence_source="http://example.invalid/delivery", evidence_content="registered unavailable source")
    invoice = _record("invoice", _id("INV"), order_id)
    txs = _publish(contract, account, order, delivery, invoice)
    before = json.loads(contract.get_remaining_quantities(args=[order_id]).call())
    failed = _submit(contract, "reconcile", [delivery["record_id"], invoice["record_id"]], account,
                     should_succeed=False)
    txs.append(failed)
    after = json.loads(contract.get_remaining_quantities(args=[order_id]).call())
    assert after == before
    _record_scenario("negative_external_failure_fail_closed", txs, {"remaining_before": before, "remaining_after": after,
                                                                    "tx_execution_result_name": failed.get("tx_execution_result_name")})
