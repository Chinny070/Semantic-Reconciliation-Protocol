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
- Latest commit at deployment: `2700b3970f9336499cfc11c7b4a3e9bc56c48e87`.
- Later read-only fetch confirmed local `HEAD` equals `origin/main` at that commit.
- Contract source Git blob: `c0165e348d30e65d8f8a7648d9661e5c1090d540`.

## Latest deployment observed

- Network: Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`.
- Address: `0xFdDaDD2732f78fFD0aCECd27c2c56704171437f0`.
- Deployment transaction: `0xbe1a4c599aae5c80b6d04aecba3786baa03d527fae97576c3bb468dc7ae6a647`.
- Receipt queried at `FINALIZED`: confirmed; result `MAJORITY_AGREE` with five validator votes.
- On-chain schema retrieved: 12 methods.
- Exact source parity, live application scenarios, and Explorer proof for this latest address: **not verified**.

## Live scenario evidence and limits

A full seven-case run was attempted against the immediately preceding deployment, `0x577627dc60776751bF4c5070144fe701ef6312C0`, which had the same deterministic arithmetic/state logic and latest-certificate view but predates the final prompt clarification for packaging classification. Six scenarios passed with finalized transactions: rendered-evidence semantic match, partial fulfillment, allowed substitution, unauthorized substitution, disguised duplicate prevention, and fail-closed external-evidence failure. Packaging did not yield a certificate, so it did not pass on that deployment. The duplicate certificate was separately retrieved and confirmed zero consumption with `DUPLICATE_BILLING_ATTEMPT`.

The latest deployment was then tested, but the Studionet RPC closed connections and subsequently timed out during the packaging-only retry before a transaction was submitted. Therefore none of the prior address’s scenario results are represented as latest-address proof, and the final packaging prompt fix remains unverified live.

## Required before freeze

1. Restore Studionet access and run the complete seven-case suite against `0xFdDaDD2732f78fFD0aCECd27c2c56704171437f0`; resolve any consensus or state defect without relaxing validator equivalence.
2. Retrieve the latest deployed code and compare it byte-for-byte with the source commit.
3. Verify a public Explorer page/transaction trail.
4. Complete typed deterministic enforcement for commercial threshold obligations, plus order correction/reversal and required challenge/forged-leader live audits where applicable.
5. Complete a clean-clone run and rejection-oriented steward audit; update this record only from observed results.

Do not call this candidate green, finalized for submission, or frozen until those gates are verified.
