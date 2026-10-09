# Deployment

## Network

Canonical target: GenLayer Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`. The installed CLI resolved the matching GenLayer Studio Network immediately before deployment.

## Latest deployment

- Source commit: `2700b3970f9336499cfc11c7b4a3e9bc56c48e87` (`main`)
- Deployment transaction: `0xbe1a4c599aae5c80b6d04aecba3786baa03d527fae97576c3bb468dc7ae6a647`
- Contract address: `0xFdDaDD2732f78fFD0aCECd27c2c56704171437f0`
- Receipt: `FINALIZED`; deployment consensus: `MAJORITY_AGREE`; five validator votes were recorded.
- Retrieved schema: 12 methods (7 views and 5 writes), including `get_latest_reconciliation_for_order`.
- Explorer evidence and deployed-source parity for this exact deployment are **not verified**. Earlier deployed versions are historical and are not interchangeable with this address.

## Release status

This deployment is an unaccepted release candidate, not a frozen or submission-ready build. See [release verification](RELEASE_CANDIDATE_VERIFICATION.md) and [steward rejection audit](STEWARD_REJECTION_AUDIT.md) for the remaining gates. The live RPC became unavailable during the final packaging retry, so the latest source still needs its full live suite and source-parity check.
