"""Opt-in live Studionet test. Never runs as part of Direct Mode."""
import json
import os
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


ADDRESS = os.environ.get("SRP_CANONICAL_ADDRESS")
pytestmark = pytest.mark.skipif(not ADDRESS, reason="canonical Studionet deployment address not configured")


def test_canonical_contract_schema_and_certificate_view():
    contract = get_contract_factory("SemanticReconciliation").at(ADDRESS)
    assert contract.get_reconciliation_certificate("missing").call() == ""
    assert contract.is_reconciliation_clear("missing").call() is False


def test_live_reconciliation_scenarios_are_recorded_not_assumed():
    evidence_path = os.environ.get("SRP_LIVE_EVIDENCE_JSON")
    assert evidence_path, "set SRP_LIVE_EVIDENCE_JSON after executing live scenarios"
    with open(evidence_path, encoding="utf-8") as stream:
        evidence = json.load(stream)
    for scenario in ("semantic_match", "packaging", "partial", "substitution_rejected", "duplicate_blocked", "negative_fail_closed"):
        assert scenario in evidence
        assert evidence[scenario].get("transaction_hash")
        assert evidence[scenario].get("stored_result") is not None
