# Deployment

## Canonical Studionet deployment

- Network: GenLayer Studionet, chain ID `61999`; RPC `https://studio.genlayer.com/api`.
- Source commit: `3c507a8eb875d8988ce8c14962eafd003fb2e195`.
- Deployment transaction: [`0xae1dffc9d421d832872762c7c453c2bb3fa4975ce4a5e164cca8ea14b9d01abc`](https://explorer-studio.genlayer.com/tx/0xae1dffc9d421d832872762c7c453c2bb3fa4975ce4a5e164cca8ea14b9d01abc).
- Contract: [`0xEdcdC09588C71aDD0B10396A07Bb022a4a3b3D56`](https://explorer-studio.genlayer.com/address/0xEdcdC09588C71aDD0B10396A07Bb022a4a3b3D56).
- Receipt: `FINALIZED`; GenLayer result `MAJORITY_AGREE`; five validators committed/revealed (three agree, two idle).
- Explorer transaction page independently shows `FINALIZED`, type `Deploy`, consensus `Accepted`, and the same contract in the linked `To` field. Explorer displayed the contract bytecode input. The linked address route was exposed by the page; its separate detail view did not finish rendering during verification.
- On-chain schema: 14 methods (9 views and 5 writes).
- Deployed source parity: retrieved source equals local `contracts/semantic_reconciliation.py` after newline normalization. Both SHA-256 values: `d37eac79db186ab0c7eecd51ae0f86cb6f3ebf4570945f2c54b5a94e1fdd7460`.
- Contract Git blob for the deployed source commit: `9006c908def47a47137ce952ba6a37d8b4bb371b`.

The source has not changed since deployment. Later release documentation and live-evidence commits do not change the deployed contract blob. Older deployment addresses in Git history are historical and are not substitutes for this canonical address.

## Release status

All thirteen required live scenarios have verified expected outcomes, and all recorded writes finalized with `MAJORITY_AGREE`. Final release gates remain: push the evidence/docs commit, verify it from a clean clone, and confirm the worktree is clean. See [live evidence ledger](LIVE_EVIDENCE.md) and [steward rejection audit](STEWARD_REJECTION_AUDIT.md) for the evidence and bounded v1 limitations.
