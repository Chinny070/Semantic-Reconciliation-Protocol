import json

import pytest

from conftest import order, record


@pytest.mark.parametrize("bad", [
    {"order_id": "PO", "counterparty": "x", "lines": [], "obligations": []},
    {"order_id": "PO", "counterparty": "x", "lines": [{"line_id": "x", "quantity": True}], "obligations": []},
    {"order_id": "PO", "counterparty": "x", "lines": [{"line_id": "x", "quantity": -1}], "obligations": []},
])
def test_bad_orders_rejected(system, bad):
    c, vm = system
    with vm.expect_revert():
        c.create_order(json.dumps(bad))


def test_duplicate_record_id_rejected(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    with vm.expect_revert("delivery id already exists"):
        c.register_delivery(json.dumps(record("delivery", "D-1")))


def test_unknown_successor_predecessor_rejected(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    with vm.expect_revert("invalid delivery predecessor"):
        c.register_delivery(json.dumps(record("delivery", "D-2", predecessor="missing")))


def test_successor_cannot_cross_order_lineage(system):
    c, vm = system
    c.create_order(json.dumps(order("PO-1")))
    other = order("PO-2")
    c.create_order(json.dumps(other))
    c.register_delivery(json.dumps(record("delivery", "D-1", order_id="PO-1")))
    with vm.expect_revert("invalid delivery predecessor"):
        c.register_delivery(json.dumps(record("delivery", "D-2", order_id="PO-2", predecessor="D-1")))


def test_corrected_invoice_can_preserve_invoice_number_and_immutable_lineage(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    original = record("invoice", "I-1", description="original invoice evidence")
    c.register_invoice(json.dumps(original))
    corrected = record("invoice", "I-2", predecessor="I-1", description="corrected invoice evidence")
    corrected["invoice_number"] = original["invoice_number"]
    c.register_invoice(json.dumps(corrected))
    assert c.get_successor("I", "I-1") == "I-2"
    assert json.loads(c.get_invoice_record("I-1"))["record_id"] == "I-1"
    assert json.loads(c.get_invoice_record("I-2"))["predecessor_id"] == "I-1"


def test_more_than_sixty_four_invoice_records_are_rejected(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    for index in range(64):
        c.register_invoice(json.dumps(record("invoice", "I-" + str(index), description="invoice " + str(index))))
    with vm.expect_revert("invoice history bound reached"):
        c.register_invoice(json.dumps(record("invoice", "I-overflow", description="overflow")))


def test_more_than_sixty_four_orders_are_rejected(system):
    c, vm = system
    for index in range(64):
        c.create_order(json.dumps(order("PO-" + str(index))))
    with vm.expect_revert("order history bound reached"):
        c.create_order(json.dumps(order("PO-overflow")))


def test_more_than_sixty_four_delivery_records_are_rejected(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    for index in range(64):
        c.register_delivery(json.dumps(record("delivery", "D-" + str(index), description="delivery " + str(index))))
    with vm.expect_revert("delivery history bound reached"):
        c.register_delivery(json.dumps(record("delivery", "D-overflow", description="overflow")))


def test_unrelated_caller_cannot_register_records(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    vm.sender = "0x0000000000000000000000000000000000000007"
    with vm.expect_revert("caller is not an order participant"):
        c.register_delivery(json.dumps(record("delivery", "D-1")))


def _cross_party_order(c, vm):
    buyer = "0x0000000000000000000000000000000000000001"
    seller = "0x0000000000000000000000000000000000000002"
    vm.sender = buyer
    definition = order()
    definition["counterparty"] = seller
    c.create_order(json.dumps(definition))
    return buyer, seller


def test_record_registrar_is_contract_bound_and_cannot_be_forged(system):
    c, vm = system
    buyer, seller = _cross_party_order(c, vm)
    vm.sender = seller
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    c.register_invoice(json.dumps(record("invoice", "I-1")))
    delivery = json.loads(c.get_delivery_record("D-1"))
    invoice = json.loads(c.get_invoice_record("I-1"))
    assert delivery["registered_by"] == seller
    assert invoice["registered_by"] == seller
    forged = record("delivery", "D-forged")
    forged["registered_by"] = buyer
    with vm.expect_revert("invalid delivery fields"):
        c.register_delivery(json.dumps(forged))
    forged_invoice = record("invoice", "I-forged")
    forged_invoice["registered_by"] = buyer
    with vm.expect_revert("invalid invoice fields"):
        c.register_invoice(json.dumps(forged_invoice))


def test_correction_ownership_requires_the_original_record_registrar(system):
    c, vm = system
    buyer, seller = _cross_party_order(c, vm)
    vm.sender = seller
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    original_invoice = record("invoice", "I-1")
    c.register_invoice(json.dumps(original_invoice))

    vm.sender = buyer
    delivery_successor = record("delivery", "D-BUYER", predecessor="D-1", description="buyer correction")
    invoice_successor = record("invoice", "I-BUYER", predecessor="I-1", description="buyer correction")
    with vm.expect_revert("delivery successor registrar mismatch"):
        c.register_delivery(json.dumps(delivery_successor))
    with vm.expect_revert("invoice successor registrar mismatch"):
        c.register_invoice(json.dumps(invoice_successor))
    assert c.get_successor("D", "D-1") == ""
    assert c.get_successor("I", "I-1") == ""

    vm.sender = seller
    delivery_successor = record("delivery", "D-SELLER", predecessor="D-1", description="seller correction")
    invoice_successor = record("invoice", "I-SELLER", predecessor="I-1", description="seller correction")
    invoice_successor["invoice_number"] = original_invoice["invoice_number"]
    c.register_delivery(json.dumps(delivery_successor))
    c.register_invoice(json.dumps(invoice_successor))
    assert c.get_successor("D", "D-1") == "D-SELLER"
    assert c.get_successor("I", "I-1") == "I-SELLER"


def test_superseded_original_remains_readable_but_cannot_reconcile(system):
    c, vm = system
    buyer, seller = _cross_party_order(c, vm)
    vm.sender = seller
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    c.register_invoice(json.dumps(record("invoice", "I-1")))
    c.register_delivery(json.dumps(record("delivery", "D-2", predecessor="D-1", description="corrected delivery")))
    assert c.get_successor("D", "D-1") == "D-2"
    assert json.loads(c.get_delivery_record("D-1"))["registered_by"] == seller
    assert json.loads(c.get_delivery_record("D-1"))["record_id"] == "D-1"
    vm.sender = buyer
    with vm.expect_revert("superseded records cannot reconcile"):
        c.reconcile("D-1", "I-1")


def test_conflicting_participant_successors_cannot_replace_or_branch_record(system):
    c, vm = system
    buyer, seller = _cross_party_order(c, vm)
    vm.sender = seller
    c.register_delivery(json.dumps(record("delivery", "D-1")))

    vm.sender = buyer
    with vm.expect_revert("delivery successor registrar mismatch"):
        c.register_delivery(json.dumps(record("delivery", "D-BUYER", predecessor="D-1")))
    vm.sender = seller
    c.register_delivery(json.dumps(record("delivery", "D-SELLER", predecessor="D-1", description="seller correction")))

    vm.sender = buyer
    with vm.expect_revert("invalid delivery predecessor"):
        c.register_delivery(json.dumps(record("delivery", "D-BRANCH", predecessor="D-1", description="competing buyer correction")))
    vm.sender = seller
    with vm.expect_revert("invalid delivery predecessor"):
        c.register_delivery(json.dumps(record("delivery", "D-SECOND", predecessor="D-1", description="second seller correction")))
    assert c.get_successor("D", "D-1") == "D-SELLER"


def test_nonparticipant_cannot_trigger_semantic_reconciliation(system):
    c, vm = system
    _, seller = _cross_party_order(c, vm)
    vm.sender = seller
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    c.register_invoice(json.dumps(record("invoice", "I-1")))
    vm.sender = "0x0000000000000000000000000000000000000007"
    with vm.expect_revert("caller is not an order participant"):
        c.reconcile("D-1", "I-1")


def test_certificate_reports_semantic_result_without_claiming_bilateral_acceptance(system):
    c, vm = system
    buyer, seller = _cross_party_order(c, vm)
    vm.sender = seller
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    c.register_invoice(json.dumps(record("invoice", "I-1")))
    vm.sender = buyer
    vm.mock_llm(r"You are an independent semantic commercial-record classifier", json.dumps({
        "edges": [{"order_line_id": "O1", "delivery_line_id": "D1", "invoice_line_id": "I1",
                   "relation": "ALLOWED_EQUIVALENT", "substitution": "ALLOWED_EQUIVALENT",
                   "duplicate_class": "DISTINCT_CHARGE"}],
        "obligations": {}, "evidence_sufficient": True,
    }))
    certificate = json.loads(c.reconcile("D-1", "I-1"))
    assert certificate["reconciliation_status"] == "MATCHED"
    assert certificate["record_authorities"] == {"delivery": seller, "invoice": seller}
    assert certificate["commercial_acceptance_status"] == "NOT_ASSESSED"


def test_exact_duplicate_invoice_content_rejected(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    first = record("invoice", "I-1")
    c.register_invoice(json.dumps(first))
    duplicate = record("invoice", "I-2")
    with vm.expect_revert("duplicate invoice evidence"):
        c.register_invoice(json.dumps(duplicate))


def test_exact_duplicate_delivery_content_rejected(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    with vm.expect_revert("duplicate delivery evidence"):
        c.register_delivery(json.dumps(record("delivery", "D-2")))
