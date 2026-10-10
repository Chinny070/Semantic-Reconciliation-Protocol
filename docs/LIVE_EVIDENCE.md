# Studionet live evidence ledger

## Canonical deployment

The current candidate is deployed to Studionet contract [`0x6cf5c63E9f5CddC9a113776Ea91b891907a90Fa7`](https://explorer-studio.genlayer.com/address/0x6cf5c63E9f5CddC9a113776Ea91b891907a90Fa7) from source commit `948156b`. Deployment transaction [`0x7a1abe0448c2801bf4f05f32d230410e5e2c59b2becffbe4a9e2f2c75fc549be`](https://explorer-studio.genlayer.com/tx/0x7a1abe0448c2801bf4f05f32d230410e5e2c59b2becffbe4a9e2f2c75fc549be) finalized with `MAJORITY_AGREE`.

Retrieved deployed source matched the local source after newline normalization. Both SHA-256 values were `fc2c35d9b4c158ada8735106fbb00362c5a4a6bf6ac21c8af62d173d2bf3573b`.

## Live scenario progress

All fifteen required scenarios have verified expected outcomes on this deployment. All expected/observed comparisons passed and the machine-readable artifact contains the transaction and readback evidence for every scenario.

| Scenario | Verified observation | State |
|---|---|---|
| Rendered public evidence semantic match | MATCHED; consumed 10 | Verified |
| Exact item | MATCHED / EXACT_MATCH; consumed 10 | Verified |
| Packaging equivalence | MATCHED / PACKAGING_EQUIVALENT; consumed 24 | Verified |
| Partial fulfillment | PARTIAL_MATCH; consumed 4 | Verified |
| Allowed equivalent substitution | MATCHED / ALLOWED_EQUIVALENT; consumed 10 | Verified |
| Unauthorized substitution | INCONCLUSIVE / UNAUTHORIZED_SUBSTITUTION; consumed 0 | Verified |
| Inferior substitution | INCONCLUSIVE / INFERIOR_SUBSTITUTION; consumed 0 | Verified |
| Ambiguous substitution | INCONCLUSIVE / AMBIGUOUS; consumed 0 | Verified |
| Disguised duplicate replay | First use consumed 10; replay consumed 0 and recorded `DUPLICATE_BILLING_ATTEMPT` | Verified |
| Quantity shortfall | PARTIAL_MATCH / QUANTITY_SHORTFALL; consumed 4 | Verified |
| Price obligation failure | INCONCLUSIVE / OBLIGATION_EXCEPTION; consumed 0 | Verified |
| Invoice correction successor | MATCHED; predecessor/successor lineage read; consumed 10 | Verified |
| External evidence unavailable | EVIDENCE_UNAVAILABLE; consumed 0, no semantic edge | Verified |
| Multiline partial with unmatched order line | PARTIAL_MATCH with explicit unmatched order node | Verified |
| Sustained challenge | provisional consumption reversed; state `VOIDED_BY_CHALLENGE` | Verified |

Machine-readable evidence is [`artifacts/studionet_live_evidence.json`](../artifacts/studionet_live_evidence.json). It contains 15 verified scenario records, all on the same address. `gltest` clears the artifact directory on startup, so future runs must preserve and merge existing records before replacing this release artifact.
