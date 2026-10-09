# Release candidate verification record

Date: 2026-10-09. Status: **NOT FROZEN**.

## Local gates verified

- Python 3.12.10; `genlayer-py` 0.16.3; `genlayer-test` 0.29.2; `genvm-linter` 0.11.0.
- Direct Mode: 42 passed.
- GenVM AST lint: 3 checks passed.
- Contract schema validation: 12 methods (7 views, 5 writes).
- Supplemental typecheck: no errors.
- Fixture/protocol preflight: passed.
- Integration suite collection: seven Studionet scenarios collected.

## GitHub

- Repository: https://github.com/Chinny070/Semantic-Reconciliation-Protocol
- Branch: `main`.
- Latest source commit at deployment: `26b55af617c2a2844b44001fa49c4ea485596238`.
- Local `HEAD` and `origin/main` both resolve to that commit.
- Contract source was retrieved from the deployed address and compared byte-for-byte after line-ending normalization. Both normalized source SHA-256 values are `da277dea8a0db7f7cd94f5d6c592835ef06095aff7673de9ff2563ff0114f3ff`.

## Latest deployment observed

- Network: Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`.
- Address: `0xAa78272Caf6EAf7e523E78768319fBc2a65eF795`.
- Deployment transaction: `0x024a2bf6243324b76de4b7a1234a2a428402341f19ac625c9c28d6c6614b0821`.
- Receipt queried at `FINALIZED`: confirmed; result `MAJORITY_AGREE` with five validator votes.
- On-chain schema retrieved: 12 methods.
- Exact source parity: **verified** as above. Explorer proof: **not verified**.

## Live scenario evidence and limits

A complete integration run was attempted against this exact address. Four scenarios passed and wrote independently checked certificates: rendered-evidence semantic reconciliation, packaging/unit equivalence, partial fulfillment, and permitted equivalent substitution. Every transaction in those four cases was `FINALIZED` with `MAJORITY_AGREE`. The certificates reported, respectively: `R3 MATCHED`/10 consumed; `R4 MATCHED`/24 base units consumed with `PACKAGING_EQUIVALENT`; `R5 PARTIAL_MATCH`/4 consumed; and `R6 MATCHED`/10 consumed with `ALLOWED_EQUIVALENT`.

The unauthorized-substitution case also finalized, with three disagreeing votes and two idle validators (receipt result `MAJORITY_DISAGREE`). The leader output and stored certificate show `ALLOWED_SUPERIOR`, zero consumed, `INCONCLUSIVE`, and `UNAUTHORIZED_SUBSTITUTION` under an `EXACT_REQUIRED` order. This is fail-closed, but validator equivalence did not agree, so the scenario is not counted green. The disguised duplicate case started but later RPC receipt polling timed out; its isolated run had previously passed on this deployment with seven finalized `MAJORITY_AGREE` transactions and `DUPLICATE_BILLING_ATTEMPT`, zero consumed. The external-route failure case did not start: schema retrieval failed because the Studionet RPC was unavailable. Preserve these as incomplete, not latest-suite passes.

## Required before freeze

1. Restore Studionet access; rerun unauthorized substitution until validators agree on a typed fail-closed finding or identify/fix validator inconsistency. Rerun duplicate and external-route failure gates against this address.
2. Verify a public Explorer page/transaction trail. A direct open of the CLI-reported Explorer URL at this address was inaccessible through the available browser lookup, so Explorer proof remains unverified.
3. Complete typed deterministic enforcement for commercial threshold obligations, plus order correction/reversal and required challenge/forged-leader live audits where applicable.
4. Complete a clean-clone run at `26b55af` and rejection-oriented steward audit; update this record only from observed results.

## Evidence identifiers

- Deployment receipt: `0x024a2bf6243324b76de4b7a1234a2a428402341f19ac625c9c28d6c6614b0821`.
- Unauthorized-substitution disagreement receipt: `0x074dff0f3347ac148be92f7665672439a7a34961365bcc2b8576a43a9aaf2a2c`.
- External-route failure test retry: could not retrieve contract schema (`gltest` reported failure across default, hosted Studio, and local clients); no scenario transaction was submitted.
- Current-address successful scenario transactions and certificate details: [live evidence ledger](LIVE_EVIDENCE.md).

Do not call this candidate green, finalized for submission, or frozen until those gates are verified.
