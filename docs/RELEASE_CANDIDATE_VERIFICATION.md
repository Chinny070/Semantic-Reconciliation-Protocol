# Release candidate verification record

Date: 2026-10-09 (workspace client date)

## Verified locally

- Python 3.12.10
- `genlayer-py` 0.16.3
- `genlayer-test` 0.29.2
- `genvm-linter` 0.11.0
- Direct Mode: 22 passed (pickling checks enabled).
- GenVM AST lint: passed (3 checks; no warnings).
- GenVM schema: passed; nine public methods reported.
- SDK validation: passed.
- Supplemental Pyright typecheck: passed with no type errors.
- Fixture preflight: order, delivery, and invoice passed.

## Not verified

- Final-source lint/check: passed (AST 3 checks and SDK schema/validation, 9 methods).
- Supplemental typecheck: passed with no type errors.
- Fixture preflight: passed for order, delivery, and invoice.
- Real independent validator consensus or forged-leader rejection on a network.
- Public web evidence retrieval/rendering.
- Studionet integration, deployment, finality, canonical address, Explorer proof or live scenarios.
- GitHub history/default branch, push, remote source parity, clean clone.

GitHub clone failed before transfer because the host denied a connection to `github.com:443`. Do not treat this as a repository or contract failure. Do not submit until every applicable unverified gate is green.

The Studionet connectivity check to `studio.genlayer.com:443` also failed before transaction submission. Git has no initialized repository metadata in this workspace. The available GitHub CLI account is configured but its token is invalid; no token value was read or printed.
