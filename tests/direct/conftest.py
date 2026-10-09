import json
import sys
from pathlib import Path

import pytest
from gltest.direct import VMContext, deploy_contract
from gltest.direct.sdk_loader import setup_sdk_paths

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "semantic_reconciliation.py"
sys.path.insert(0, str(ROOT))


@pytest.fixture
def system():
    vm = VMContext()
    vm.check_pickling = True
    setup_sdk_paths(CONTRACT)
    with vm.activate():
        contract = deploy_contract(CONTRACT, vm)
        yield contract, vm


def order(order_id="PO-1", quantity=10, policy="EQUIVALENT_ALLOWED", max_price=100, obligations=None):
    return {
        "order_id": order_id,
        "counterparty": "0x0000000000000000000000000000000000000002",
        "lines": [{
            "line_id": "O1", "description": "Portland cement 42.5", "unit": "bottle",
            "quantity": quantity, "max_unit_price_minor": max_price, "charge_class": "GOODS", "deadline_timestamp": 0,
            "unit_conversions": [{"unit": "bottle", "numerator": 1, "denominator": 1}],
            "substitution_policy": policy, "named_alternatives": [], "criticality": "STANDARD",
        }],
        "obligations": obligations or [],
    }


def record(kind, record_id, order_id="PO-1", quantity=10, description="OPC grade 42.5", predecessor=None, price=90, unit="bottle"):
    line = {
        "line_id": kind[0].upper() + "1", "description": description, "unit": unit,
        "quantity": quantity, "evidence_ref": kind,
    }
    if kind == "invoice":
        line.update({"unit_price_minor": price, "charge_class": "GOODS"})
    result = {
        "record_id": record_id, "order_id": order_id, "predecessor_id": predecessor,
        "source_reference": "source:" + record_id, "lines": [line],
        "evidence": {"retrieval_kind": "STRUCTURED_FIXTURE", "source": "fixture:" + record_id, "content": description},
    }
    if kind == "invoice":
        result["invoice_number"] = "NUMBER:" + record_id
    return result


def proposal(relation="ALLOWED_EQUIVALENT", substitution="ALLOWED_EQUIVALENT", duplicate="DISTINCT_CHARGE", sufficient=True):
    return {
        "edges": [{"order_line_id": "O1", "delivery_line_id": "D1", "invoice_line_id": "I1",
                   "relation": relation, "substitution": substitution, "duplicate_class": duplicate}],
        "obligations": {}, "evidence_sufficient": sufficient,
    }


def mock_matching(vm, value):
    vm.mock_llm(r"You are an independent semantic commercial-record classifier", json.dumps(value))
