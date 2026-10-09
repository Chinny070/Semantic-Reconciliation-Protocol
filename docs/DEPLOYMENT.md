# Deployment

## Network

Canonical target: GenLayer Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`. The installed CLI resolved the matching GenLayer Studio Network immediately before deployment.

## Latest deployment

- Source commit: `26b55af617c2a2844b44001fa49c4ea485596238` (`main`)
- Deployment transaction: `0x024a2bf6243324b76de4b7a1234a2a428402341f19ac625c9c28d6c6614b0821`
- Contract address: `0xAa78272Caf6EAf7e523E78768319fBc2a65eF795`
- Receipt: `FINALIZED`; deployment consensus: `MAJORITY_AGREE`; five validator votes were recorded.
- Retrieved schema: 12 methods (7 views and 5 writes), including `get_latest_reconciliation_for_order`.
- Deployed-source parity is verified byte-for-byte after line-ending normalization (SHA-256 `da277dea8a0db7f7cd94f5d6c592835ef06095aff7673de9ff2563ff0114f3ff` for both local and deployed source). Explorer evidence remains unverified. Earlier deployed versions are historical and are not interchangeable with this address.

## Release status

This deployment is an unaccepted release candidate, not a frozen or submission-ready build. Four current-address live scenarios passed, one reached a finalized fail-closed disagreement, one timed out while polling, and one could not start during RPC unavailability. See [release verification](RELEASE_CANDIDATE_VERIFICATION.md) and [steward rejection audit](STEWARD_REJECTION_AUDIT.md) for the remaining gates.
