import json
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "protocol_helpers", Path(__file__).resolve().parents[2] / "contracts" / "protocol.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
_validate_proposal = module.validate_proposal
from conftest import order, proposal, record


def test_typed_proposal_rejects_unknown_ids_and_enum():
    o, d, i = order(), record("delivery", "D-1"), record("invoice", "I-1")
    forged = proposal()
    forged["edges"][0]["order_line_id"] = "invented"
    try:
        _validate_proposal(forged, o, d, i)
        assert False, "unknown ID accepted"
    except ValueError:
        pass
    forged = proposal()
    forged["edges"][0]["relation"] = "APPROVE_ALL"
    try:
        _validate_proposal(forged, o, d, i)
        assert False, "unknown enum accepted"
    except ValueError:
        pass


def test_validator_rejects_forged_leader_result():
    o, d, i = order(), record("delivery", "D-1"), record("invoice", "I-1")
    try:
        _validate_proposal({"edges": [], "obligations": {}, "evidence_sufficient": True}, o, d, i)
        assert False, "empty forged answer unexpectedly validated as a match"
    except ValueError:
        pass


def test_bool_is_not_accepted_as_integer_quantity(system):
    c, vm = system
    import json
    bad = order()
    bad["lines"][0]["quantity"] = True
    with vm.expect_revert("invalid ordered quantity"):
        c.create_order(json.dumps(bad))


def test_proposal_rejects_invented_invoice_line_and_float_quantity(system):
    o, d, i = order(), record("delivery", "D-1"), record("invoice", "I-1")
    forged = proposal()
    forged["edges"][0]["invoice_line_id"] = "invented"
    try:
        _validate_proposal(forged, o, d, i)
        assert False, "invented invoice line accepted"
    except ValueError:
        pass


def test_proposal_rejects_reusing_one_source_line_for_two_edges():
    o, d, i = order(), record("delivery", "D-1"), record("invoice", "I-1")
    forged = proposal()
    second = dict(forged["edges"][0])
    second["invoice_line_id"] = "I2"
    i["lines"].append(dict(i["lines"][0], line_id="I2"))
    forged["edges"].append(second)
    try:
        _validate_proposal(forged, o, d, i)
        assert False, "reused delivery capacity accepted"
    except ValueError:
        pass
    bad = order()
    bad["lines"][0]["quantity"] = 1.0
    try:
        module.validate_order(json.dumps(bad))
        assert False, "float quantity accepted"
    except ValueError:
        pass
