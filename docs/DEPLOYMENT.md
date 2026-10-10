# Deployment

## Corrected Studionet candidate

- Network: GenLayer Studionet, chain ID `61999`; RPC `https://studio.genlayer.com/api`.
- Source commit deployed: `948156b` (`Harden reconciliation lifecycle and multiline graph`).
- Deployment transaction: [`0x7a1abe0448c2801bf4f05f32d230410e5e2c59b2becffbe4a9e2f2c75fc549be`](https://explorer-studio.genlayer.com/tx/0x7a1abe0448c2801bf4f05f32d230410e5e2c59b2becffbe4a9e2f2c75fc549be).
- Contract: [`0x6cf5c63E9f5CddC9a113776Ea91b891907a90Fa7`](https://explorer-studio.genlayer.com/address/0x6cf5c63E9f5CddC9a113776Ea91b891907a90Fa7).
- Deployment receipt: `FINALIZED`, `MAJORITY_AGREE`, five revealed validator slots.
- Retrieved deployed source and local source have normalized SHA-256 `fc2c35d9b4c158ada8735106fbb00362c5a4a6bf6ac21c8af62d173d2bf3573b` and equal normalized content.
- The corrected source exposes 16 methods: 10 views and 6 writes, including reconciliation state and finalization.

The deployment address above is the only address for this release. Earlier addresses and evidence files are historical and must not be used to represent the corrected contract.

## Verification status

The local release gates are green from a clean checkout at `948156b`: pinned dependency parity, Direct Mode, GenVM lint, typecheck, protocol preflight, and mutation checks. The live scenario ledger is updated only from finalized receipts against the address above. See [live evidence](LIVE_EVIDENCE.md) and [release verification](RELEASE_CANDIDATE_VERIFICATION.md).
