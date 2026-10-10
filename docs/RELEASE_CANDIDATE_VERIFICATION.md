# Release candidate verification

Verification date: 2026-10-10. The candidate is deployed on Studionet at `0x6cf5c63E9f5CddC9a113776Ea91b891907a90Fa7` (chain ID `61999`). The complete live matrix, source parity, pushed HEAD, and fresh-clone local gates passed.

## Local validation

- Direct Mode: 74 tests passed, with pickling enabled.
- GenVM AST lint: 3 checks passed.
- Contract schema: 16 methods (10 views and 6 writes).
- Supplemental typecheck and protocol preflight passed.
- Integration test collection: 15 scenarios.

## Git and deployment

- Repository: `https://github.com/Chinny070/Semantic-Reconciliation-Protocol`; GitHub reports `PUBLIC`, default branch `main`.
- Deployed contract source commit: `948156b`.
- Deployment transaction: `0x7a1abe0448c2801bf4f05f32d230410e5e2c59b2becffbe4a9e2f2c75fc549be`.
- Contract address: `0x6cf5c63E9f5CddC9a113776Ea91b891907a90Fa7`.
- Deployment receipt: `FINALIZED`, `MAJORITY_AGREE`; five validators committed/revealed, three agreed and two were idle.
- Explorer proof: [deployment transaction](https://explorer-studio.genlayer.com/tx/0x7a1abe0448c2801bf4f05f32d230410e5e2c59b2becffbe4a9e2f2c75fc549be) finalized with `MAJORITY_AGREE`.
- On-chain schema: 16 methods (10 views and 6 writes).
- Source parity: retrieved deployed source matched after newline normalization; both SHA-256 values are `fc2c35d9b4c158ada8735106fbb00362c5a4a6bf6ac21c8af62d173d2bf3573b`.

## Live scenarios

All fifteen scenario records have verified expectations and finalized/readback evidence on the same canonical address. Transaction IDs, certificates, before/after ledgers, and evidence sources are included. A record audit confirmed every expected outcome and address.

The full set includes rendered-evidence semantic match, exact item, packaging equivalence, partial fulfillment, allowed equivalent substitution, unauthorized substitution, inferior substitution, ambiguous substitution, disguised duplicate replay, quantity shortfall, deterministic price obligation failure, invoice correction successor, external evidence unavailable, multiline unmatched order handling, and sustained challenge reversal. All 15 expected/observed comparisons passed.

## Adversarial and scope audit

Direct Mode exercises forged well-formed and malformed leader proposals, invented or omitted IDs, unsupported enums, conflicting semantic outputs, error wrappers, and fail-closed substitution behavior. GenLayer output controls semantic classification only; deterministic contract code controls ratios, quantities, prices, obligations, IDs, duplicate use, and state transitions.

Correction behavior is bounded in v1: orders are sealed and immutable; delivery and invoice successors are supported; finalized consumption cannot be reversed. A correction requiring order amendment or reversal is unsupported. Structured fixture records are submitter-provided; the live rendered-evidence test retrieves public raw GitHub fixtures. No exhaustive patent, owner-portfolio, or ecosystem-wide novelty search is claimed.

## Release status

Frozen after the final documentation/evidence commit was pushed, a fresh clone of pushed `main` passed Direct Mode, GenVM lint/typecheck, fixture preflight, and on-chain schema retrieval, and the original worktree was confirmed clean. No external submission form has been submitted; submission materials are prepared in `SUBMISSION.md`.
