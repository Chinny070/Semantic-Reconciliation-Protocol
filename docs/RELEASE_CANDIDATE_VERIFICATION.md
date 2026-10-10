# Release candidate verification

Verification date: 2026-10-10. The candidate is deployed on Studionet at `0xEdcdC09588C71aDD0B10396A07Bb022a4a3b3D56` (chain ID `61999`). The complete live matrix, validator receipts, source parity, pushed HEAD, fresh-clone validation, and clean worktree gates passed. The candidate is frozen.

## Local validation

- Direct Mode: 52 tests passed, with pickling enabled.
- GenVM AST lint: 3 checks passed.
- Contract schema: 14 methods (9 views and 5 writes).
- Supplemental typecheck and protocol preflight passed.
- Integration test collection: 13 scenarios.

## Git and deployment

- Repository: `https://github.com/Chinny070/Semantic-Reconciliation-Protocol`; GitHub reports `PUBLIC`, default branch `main`.
- Deployed contract source commit: `3c507a8eb875d8988ce8c14962eafd003fb2e195`.
- Deployment transaction: `0xae1dffc9d421d832872762c7c453c2bb3fa4975ce4a5e164cca8ea14b9d01abc`.
- Contract address: `0xEdcdC09588C71aDD0B10396A07Bb022a4a3b3D56`.
- Deployment receipt: `FINALIZED`, `MAJORITY_AGREE`; five validators committed/revealed, three agreed and two were idle.
- Explorer proof: [deployment transaction](https://explorer-studio.genlayer.com/tx/0xae1dffc9d421d832872762c7c453c2bb3fa4975ce4a5e164cca8ea14b9d01abc) showed `FINALIZED`, `Deploy`, `Accepted`, and the contract in `To`.
- On-chain schema: 14 methods (9 views and 5 writes).
- Source parity: retrieved deployed source matched after newline normalization; both SHA-256 values are `d37eac79db186ab0c7eecd51ae0f86cb6f3ebf4570945f2c54b5a94e1fdd7460`.

## Live scenarios

All thirteen scenario records have verified expectations, finalized receipts, and `MAJORITY_AGREE` results on the same canonical address. I independently fetched all 57 unique receipts from Studionet RPC. Every receipt is finalized, has five validator vote entries, and reports majority agreement; per-validator votes, counts, and rounds are preserved in the machine-readable evidence. Transaction IDs, certificates, before/after ledgers, and evidence sources are included. A record audit confirmed every expected outcome, address, final status, and consensus result.

The full set includes rendered-evidence semantic match, exact item, packaging equivalence, partial fulfillment, allowed equivalent substitution, unauthorized substitution, inferior substitution, ambiguous substitution, disguised duplicate replay, quantity shortfall, deterministic price obligation failure, invoice correction successor, and external evidence unavailable. The two batches that completed the matrix each exited successfully; all 13 expected/observed comparisons passed.

## Adversarial and scope audit

Direct Mode exercises forged well-formed and malformed leader proposals, invented or omitted IDs, unsupported enums, conflicting semantic outputs, error wrappers, and fail-closed substitution behavior. GenLayer output controls semantic classification only; deterministic contract code controls ratios, quantities, prices, obligations, IDs, duplicate use, and state transitions.

Correction behavior is bounded in v1: orders are sealed and immutable; delivery and invoice successors are supported; finalized consumption cannot be reversed. A correction requiring order amendment or reversal is unsupported. Structured fixture records are submitter-provided; the live rendered-evidence test retrieves public raw GitHub fixtures. No exhaustive patent, owner-portfolio, or ecosystem-wide novelty search is claimed.

## Release status

Frozen after the final documentation/evidence commit was pushed, a fresh clone of pushed `main` passed Direct Mode, GenVM lint/typecheck, fixture preflight, and on-chain schema retrieval, and the original worktree was confirmed clean. No external submission form has been submitted; submission materials are prepared in `SUBMISSION.md`.
