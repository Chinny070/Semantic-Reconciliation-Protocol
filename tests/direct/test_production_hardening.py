import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone

import pytest

from conftest import mock_matching, order, proposal, record
from contracts.protocol import validate_proposal


def _two_line_order(order_id="PO-ML", quantity=10):
    value = order(order_id, quantity=quantity)
    value["lines"].append({
        **value["lines"][0],
        "line_id": "O2",
        "description": "Safety gloves nitrile",
    })
    return value


def _identity(source, content):
    return {
        "retrieval_kind": "STRUCTURED_FIXTURE",
        "source": source,
        "content_digest": hashlib.sha256(content.encode()).hexdigest(),
        "provenance_class": "PARTICIPANT_SUPPLIED",
    }


def _multi_proposal(edges, unmatched, delivery, invoice, sufficient=True):
    return {
        "edges": edges,
        "unmatched": unmatched,
        "obligations": {},
        "evidence_sufficient": sufficient,
        "evidence_identities": {
            "delivery": _identity(delivery["evidence"]["source"], delivery["evidence"]["content"]),
            "invoice": _identity(invoice["evidence"]["source"], invoice["evidence"]["content"]),
        },
    }


def test_multiline_graph_represents_unfulfilled_order_line_without_fake_source_ids():
    o = _two_line_order()
    d = record("delivery", "D-ML", order_id="PO-ML", quantity=4)
    i = record("invoice", "I-ML", order_id="PO-ML", quantity=4)
    graph = _multi_proposal([
        {"order_line_id": "O1", "delivery_line_id": "D1", "invoice_line_id": "I1",
         "relation": "ALLOWED_EQUIVALENT", "substitution": "ALLOWED_EQUIVALENT", "duplicate_class": "DISTINCT_CHARGE"},
    ], [
        {"record_type": "ORDER", "line_id": "O2", "finding": "NOT_YET_DELIVERED_OR_INVOICED"},
    ], d, i)
    assert validate_proposal(graph, o, d, i) == graph


def test_multiline_graph_represents_delivery_without_invoice_and_rejects_omission():
    o = _two_line_order()
    d = record("delivery", "D-ML", order_id="PO-ML", quantity=4)
    d["lines"].append({**d["lines"][0], "line_id": "D2", "description": "Safety gloves nitrile"})
    i = record("invoice", "I-ML", order_id="PO-ML", quantity=4)
    graph = _multi_proposal([
        {"order_line_id": "O1", "delivery_line_id": "D1", "invoice_line_id": "I1",
         "relation": "ALLOWED_EQUIVALENT", "substitution": "ALLOWED_EQUIVALENT", "duplicate_class": "DISTINCT_CHARGE"},
    ], [
        {"record_type": "ORDER", "line_id": "O2", "finding": "NOT_YET_DELIVERED_OR_INVOICED"},
        {"record_type": "DELIVERY", "line_id": "D2", "finding": "DELIVERY_WITHOUT_INVOICE"},
    ], d, i)
    validate_proposal(graph, o, d, i)
    graph["unmatched"] = graph["unmatched"][:-1]
    with pytest.raises(ValueError, match="omitted delivery-line"):
        validate_proposal(graph, o, d, i)


def test_unmatched_delivery_is_a_certificate_exception_not_silently_ignored(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    d = record("delivery", "D-1")
    d["lines"].append({**d["lines"][0], "line_id": "D2", "description": "Uninvoiced handling service", "quantity": 1})
    i = record("invoice", "I-1")
    c.register_delivery(json.dumps(d))
    c.register_invoice(json.dumps(i))
    graph = proposal()
    graph["unmatched"] = [{"record_type": "DELIVERY", "line_id": "D2", "finding": "DELIVERY_WITHOUT_INVOICE"}]
    mock_matching(vm, graph)
    cert = json.loads(c.reconcile("D-1", "I-1"))
    assert cert["consumed"][0]["quantity"] == 10
    assert cert["reconciliation_status"] == "INCONCLUSIVE"
    assert "UNINVOICED_DELIVERY" in cert["exceptions"]


def test_adversarial_graph_cannot_represent_line_as_matched_and_unmatched():
    o = order()
    d = record("delivery", "D-1")
    i = record("invoice", "I-1")
    graph = proposal()
    graph["unmatched"] = [{"record_type": "DELIVERY", "line_id": "D1", "finding": "AMBIGUOUS"}]
    with pytest.raises(ValueError, match="both matched and unmatched"):
        validate_proposal(graph, o, d, i)


def test_partial_fulfillment_across_multiple_records_conserves_order_capacity(system):
    c, vm = system
    c.create_order(json.dumps(order(quantity=10)))
    for suffix, quantity in (("A", 4), ("B", 6)):
        c.register_delivery(json.dumps(record("delivery", "D-" + suffix, quantity=quantity, description="OPC grade 42.5 lot " + suffix)))
        c.register_invoice(json.dumps(record("invoice", "I-" + suffix, quantity=quantity, description="OPC grade 42.5 lot " + suffix)))
        mock_matching(vm, proposal())
        cert = json.loads(c.reconcile("D-" + suffix, "I-" + suffix))
        assert cert["consumed"][0]["quantity"] == quantity
    ledger = json.loads(c.get_remaining_quantities("PO-1"))
    assert ledger["O1"]["reconciled"] == 10


def test_competing_invoice_allocations_cannot_overconsume_delivery_or_order(system):
    c, vm = system
    c.create_order(json.dumps(order(quantity=10)))
    c.register_delivery(json.dumps(record("delivery", "D-1", quantity=10)))
    for suffix in ("A", "B"):
        c.register_invoice(json.dumps(record("invoice", "I-" + suffix, quantity=6, description="OPC grade 42.5 charge " + suffix)))
        mock_matching(vm, proposal())
        cert = json.loads(c.reconcile("D-1", "I-" + suffix))
        assert cert["consumed"][0]["quantity"] == (6 if suffix == "A" else 4)
    ledger = json.loads(c.get_remaining_quantities("PO-1"))
    assert ledger["O1"]["reconciled"] == 10
    assert ledger["_delivery:D-1:D1"] == 10


def test_evidence_unavailable_pair_can_retry_but_definitive_result_cannot(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    c.register_invoice(json.dumps(record("invoice", "I-1")))
    unavailable = proposal(sufficient=False)
    unavailable["edges"] = []
    unavailable["unmatched"] = [
        {"record_type": "ORDER", "line_id": "O1", "finding": "INSUFFICIENT_EVIDENCE"},
        {"record_type": "DELIVERY", "line_id": "D1", "finding": "INSUFFICIENT_EVIDENCE"},
        {"record_type": "INVOICE", "line_id": "I1", "finding": "INSUFFICIENT_EVIDENCE"},
    ]
    mock_matching(vm, unavailable)
    first = json.loads(c.reconcile("D-1", "I-1"))
    assert first["reconciliation_status"] == "EVIDENCE_UNAVAILABLE"
    vm.clear_mocks()
    mock_matching(vm, proposal())
    second = json.loads(c.reconcile("D-1", "I-1"))
    assert second["consumed"][0]["quantity"] == 10
    with vm.expect_revert("record pair already reconciled"):
        c.reconcile("D-1", "I-1")


def test_certificate_binds_actual_participant_supplied_content_digest(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    d = record("delivery", "D-1", description="observed delivery bytes")
    i = record("invoice", "I-1", description="observed invoice bytes")
    c.register_delivery(json.dumps(d))
    c.register_invoice(json.dumps(i))
    mock_matching(vm, proposal())
    cert = json.loads(c.reconcile("D-1", "I-1"))
    assert cert["evidence_identities"]["delivery"]["content_digest"] == hashlib.sha256(d["evidence"]["content"].encode()).hexdigest()
    assert cert["evidence_identities"]["delivery"]["provenance_class"] == "PARTICIPANT_SUPPLIED"


def test_same_invoice_number_on_unrelated_orders_does_not_reserve_identity(system):
    c, vm = system
    c.create_order(json.dumps(order("PO-A")))
    c.create_order(json.dumps(order("PO-B")))
    first = record("invoice", "I-A", order_id="PO-A")
    second = record("invoice", "I-B", order_id="PO-B")
    second["invoice_number"] = first["invoice_number"]
    c.register_invoice(json.dumps(first))
    c.register_invoice(json.dumps(second))
    assert json.loads(c.get_invoice_record("I-B"))["order_id"] == "PO-B"


def test_named_alternative_policy_requires_both_source_descriptions_to_be_frozen(system):
    c, vm = system
    frozen = order(policy="NAMED_ALTERNATIVES_ONLY")
    frozen["lines"][0]["named_alternatives"] = ["Approved OPC 42.5 alternative"]
    c.create_order(json.dumps(frozen))
    c.register_delivery(json.dumps(record("delivery", "D-1", description="Unlisted cement")))
    c.register_invoice(json.dumps(record("invoice", "I-1", description="Unlisted cement")))
    mock_matching(vm, proposal())
    cert = json.loads(c.reconcile("D-1", "I-1"))
    assert cert["consumed"] == []
    assert "UNAUTHORIZED_SUBSTITUTION" in cert["exceptions"]


def test_finalization_closes_challenge_rights_without_changing_consumption(system, monkeypatch):
    c, vm = system
    c.create_order(json.dumps(order()))
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    c.register_invoice(json.dumps(record("invoice", "I-1")))
    mock_matching(vm, proposal())
    cert = json.loads(c.reconcile("D-1", "I-1"))
    state = json.loads(c.get_reconciliation_state(cert["reconciliation_id"]))
    future = datetime.fromtimestamp(state["challenge_deadline"], timezone.utc) + timedelta(seconds=1)

    class FutureDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return future

    module = sys.modules[type(c._instance).__module__]
    monkeypatch.setattr(module, "datetime", FutureDateTime)
    final = json.loads(c.finalize_reconciliation(cert["reconciliation_id"]))
    assert final["state"] == "FINALIZED"
    assert c.is_reconciliation_clear(cert["reconciliation_id"])
    assert json.loads(c.get_remaining_quantities("PO-1"))["O1"]["reconciled"] == 10
    edge_hash = hashlib.sha256(json.dumps(cert["semantic_edges"][0], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    with vm.expect_revert("reconciliation is not challengeable"):
        c.challenge_reconciliation(cert["reconciliation_id"], edge_hash, json.dumps({
            "retrieval_kind": "STRUCTURED_FIXTURE", "source": "fixture:late", "content": "late claim",
        }))


def test_challenged_records_recover_through_authorized_successors(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    old_d = record("delivery", "D-OLD", description="incorrect cement record")
    old_i = record("invoice", "I-OLD", description="incorrect cement record")
    c.register_delivery(json.dumps(old_d))
    c.register_invoice(json.dumps(old_i))
    mock_matching(vm, proposal())
    cert = json.loads(c.reconcile("D-OLD", "I-OLD"))
    edge_hash = hashlib.sha256(json.dumps(cert["semantic_edges"][0], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    vm.mock_llm(r"Evaluate evidence for a bounded challenge", json.dumps({
        "finding": "SUPPORTS_CHALLENGE", "evidence_sufficient": True,
    }))
    c.challenge_reconciliation(cert["reconciliation_id"], edge_hash, json.dumps({
        "retrieval_kind": "STRUCTURED_FIXTURE", "source": "fixture:correction-proof", "content": "wrong source lines",
    }))
    corrected_d = record("delivery", "D-NEW", predecessor="D-OLD", description="OPC grade 42.5 corrected")
    corrected_i = record("invoice", "I-NEW", predecessor="I-OLD", description="OPC grade 42.5 corrected")
    corrected_i["invoice_number"] = old_i["invoice_number"]
    c.register_delivery(json.dumps(corrected_d))
    c.register_invoice(json.dumps(corrected_i))
    vm.clear_mocks()
    mock_matching(vm, proposal())
    recovered = json.loads(c.reconcile("D-NEW", "I-NEW"))
    assert recovered["consumed"][0]["quantity"] == 10
    assert json.loads(c.get_remaining_quantities("PO-1"))["O1"]["reconciled"] == 10
