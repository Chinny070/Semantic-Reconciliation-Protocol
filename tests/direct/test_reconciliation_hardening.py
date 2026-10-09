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


def test_more_than_sixty_four_delivery_records_are_rejected(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    for index in range(64):
        c.register_delivery(json.dumps(record("delivery", "D-" + str(index), description="delivery " + str(index))))
    with vm.expect_revert("delivery history bound reached"):
        c.register_delivery(json.dumps(record("delivery", "D-overflow", description="overflow")))


def test_more_than_sixty_four_delivery_records_are_rejected(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    for index in range(64):
        c.register_delivery(json.dumps(record("delivery", "D-" + str(index), description="delivery " + str(index))))
    with vm.expect_revert("delivery history bound reached"):
        c.register_delivery(json.dumps(record("delivery", "D-overflow", description="overflow")))


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
