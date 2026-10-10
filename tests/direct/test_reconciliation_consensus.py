import json
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "protocol_helpers", Path(__file__).resolve().parents[2] / "contracts" / "protocol.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
_validate_proposal = module.validate_proposal
from conftest import mock_matching, order, proposal, record


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


def test_classifier_prompt_limits_edges_to_current_three_way_lines():
    from pathlib import Path

    source = Path(__file__).resolve().parents[2] / "contracts" / "semantic_reconciliation.py"
    code = source.read_text(encoding="utf-8")
    assert "Every edge must include exactly one valid order_line_id" in code
    assert "delivery_line_id, and invoice_line_id " in code
    assert "Prior consumed lines are comparison context ONLY" in code
    assert "Never fabricate a missing source ID" in code
    assert "must occur either in an edge or once in unmatched" in code
    assert "registered_by identifies only the order participant" in code
    assert "WEB_RENDERED content is independently retrieved page content" in code
    assert "not proof that the page or document is issued by an authorized commercial source" in code


def test_independent_validator_rejects_well_formed_decision_critical_forgery(system):
    c, vm = system
    c.create_order(json.dumps(order()))
    c.register_delivery(json.dumps(record("delivery", "D-1")))
    c.register_invoice(json.dumps(record("invoice", "I-1")))
    honest = proposal()
    mock_matching(vm, honest)
    c.reconcile("D-1", "I-1")
    forged_outputs = []
    unrelated = proposal(relation="UNRELATED", substitution="UNAUTHORIZED_SUBSTITUTE")
    forged_outputs.append(unrelated)
    fabricated_id = proposal()
    fabricated_id["edges"][0]["invoice_line_id"] = "FABRICATED-I9"
    forged_outputs.append(fabricated_id)
    unsupported_packaging = proposal(relation="PACKAGING_EQUIVALENT", substitution="EXACT")
    forged_outputs.append(unsupported_packaging)
    fabricated_duplicate = proposal(duplicate="POSSIBLE_DUPLICATE_OF_PRIOR_LINE")
    forged_outputs.append(fabricated_duplicate)
    omitted_critical_field = proposal()
    del omitted_critical_field["edges"][0]["duplicate_class"]
    forged_outputs.append(omitted_critical_field)
    unknown_enum = proposal()
    unknown_enum["edges"][0]["substitution"] = "MODEL_APPROVES"
    forged_outputs.append(unknown_enum)
    for forged in forged_outputs:
        assert vm.run_validator(leader_result=forged) is False, forged


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
