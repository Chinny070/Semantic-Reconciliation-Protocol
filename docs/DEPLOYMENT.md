# Deployment

## Local gates

Use pinned dependencies and run Direct Mode, schema, linter, SDK validation, and preflight before deployment. Current local package versions and results belong in the release-candidate verification record.

## Canonical Studionet

The intended stable network is Studionet at `https://studio.genlayer.com/api` (chain ID 61999). Confirm `genlayer network info` immediately before signing. Deploy only the committed green source. Record commit, contract blob hash, deployment transaction, lifecycle/finality, address, schema and Explorer URL after verification.

## Current state

Earlier GitHub clone and Studionet connectivity attempts were denied before repository transfer or transaction submission. This pass retries those gates after local remediation. No address, transaction, finality, or Explorer evidence is claimed unless the retry verifies them.
