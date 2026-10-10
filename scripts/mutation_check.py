"""Run a small, reproducible mutation suite against security-critical guards."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = (
    (
        "matched-unmatched-exclusivity",
        "protocol.py",
        'if edge_order & unmatched["ORDER"] or edge_delivery & unmatched["DELIVERY"] or edge_invoice & unmatched["INVOICE"]:',
        'if False:',
        "tests/direct/test_production_hardening.py::test_adversarial_graph_cannot_represent_line_as_matched_and_unmatched",
    ),
    (
        "order-capacity-conservation",
        "semantic_reconciliation.py",
        "amount = min(dq - prior_d, iq - prior_i, remaining)",
        "amount = min(dq, iq)",
        "tests/direct/test_production_hardening.py::test_competing_invoice_allocations_cannot_overconsume_delivery_or_order",
    ),
    (
        "challenge-ledger-reversal",
        "semantic_reconciliation.py",
        'row["reconciled"] -= amount',
        'row["reconciled"] += 0',
        "tests/direct/test_semantic_reconciliation.py::test_sustained_challenge_voids_provisional_receipt_and_releases_consumption",
    ),
)


def main() -> int:
    survivors = []
    with tempfile.TemporaryDirectory(prefix="srp-mutations-") as raw_tmp:
        base = Path(raw_tmp)
        for name, filename, needle, replacement, test_id in MUTATIONS:
            target = base / name
            shutil.copytree(ROOT / "contracts", target / "contracts")
            shutil.copytree(ROOT / "tests", target / "tests")
            shutil.copy2(ROOT / "gltest.config.yaml", target / "gltest.config.yaml")
            shutil.copy2(ROOT / "pytest.ini", target / "pytest.ini")
            source = target / "contracts" / filename
            text = source.read_text(encoding="utf-8")
            if needle not in text:
                raise RuntimeError(f"mutation target missing: {name}")
            source.write_text(text.replace(needle, replacement, 1), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "pytest", test_id, "-q"],
                cwd=target,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=180,
            )
            killed = completed.returncode != 0
            print(f"{'KILLED' if killed else 'SURVIVED'} {name}")
            if not killed:
                survivors.append(name)
    if survivors:
        print("Surviving mutations: " + ", ".join(survivors))
        return 1
    print(f"PASS {len(MUTATIONS)} security-critical mutations killed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
