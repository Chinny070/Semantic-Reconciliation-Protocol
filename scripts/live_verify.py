"""Live evidence verifier; refuses to make network claims without explicit inputs."""
import argparse
import json
import sys
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract-address", required=True)
    parser.add_argument("--deployment-tx", required=True)
    parser.add_argument("--explorer-url", required=True)
    parser.add_argument("--evidence-json", required=True, help="JSON file containing verified live receipts/results")
    args = parser.parse_args()
    try:
        with open(args.evidence_json, encoding="utf-8") as stream:
            evidence = json.load(stream)
    except (OSError, ValueError) as exc:
        print(f"UNVERIFIED: evidence input unavailable/invalid ({type(exc).__name__})", file=sys.stderr)
        return 2
    expected = {"deployment", "semantic_match", "packaging", "partial", "substitution_rejected", "duplicate_blocked", "negative_fail_closed", "source_parity"}
    if not isinstance(evidence, dict) or set(evidence) != expected:
        print("UNVERIFIED: live evidence fields incomplete", file=sys.stderr)
        return 2
    for name, entry in evidence.items():
        if not isinstance(entry, dict) or entry.get("verified") is not True:
            print(f"UNVERIFIED: {name}", file=sys.stderr)
            return 2
    if not (args.contract_address.startswith("0x") and len(args.contract_address) == 42):
        print("FAIL: contract address format invalid", file=sys.stderr)
        return 1
    try:
        request = urllib.request.Request(args.explorer_url, method="HEAD", headers={"User-Agent": "semantic-reconciliation-live-check/1"})
        with urllib.request.urlopen(request, timeout=15) as response:
            if response.status >= 400:
                raise OSError("Explorer endpoint rejected request")
    except (OSError, urllib.error.URLError) as exc:
        print(f"UNVERIFIED: Explorer reachability ({type(exc).__name__})", file=sys.stderr)
        return 2
    print("Evidence inputs are present; independently compare transactions, stored results, finality, and parity before submission.")
    print(f"contract={args.contract_address}")
    print(f"deployment_tx={args.deployment_tx}")
    print(f"explorer={args.explorer_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
