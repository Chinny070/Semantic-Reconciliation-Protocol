# Studionet live evidence ledger

## Canonical deployment

The current candidate is deployed to Studionet contract [`0xEdcdC09588C71aDD0B10396A07Bb022a4a3b3D56`](https://explorer-studio.genlayer.com/address/0xEdcdC09588C71aDD0B10396A07Bb022a4a3b3D56) from source commit `3c507a8eb875d8988ce8c14962eafd003fb2e195`. Deployment transaction [`0xae1dffc9d421d832872762c7c453c2bb3fa4975ce4a5e164cca8ea14b9d01abc`](https://explorer-studio.genlayer.com/tx/0xae1dffc9d421d832872762c7c453c2bb3fa4975ce4a5e164cca8ea14b9d01abc) finalized with `MAJORITY_AGREE`. Its Explorer transaction page showed `FINALIZED`, `Deploy`, `Accepted`, and the contract address in `To`.

Retrieved deployed source matched the local source after newline normalization. Both SHA-256 values were `d37eac79db186ab0c7eecd51ae0f86cb6f3ebf4570945f2c54b5a94e1fdd7460`; the source Git blob is `9006c908def47a47137ce952ba6a37d8b4bb371b`.

## Live scenario progress

All thirteen required scenarios have verified expected outcomes on this deployment. Every recorded write receipt is `FINALIZED` with `MAJORITY_AGREE`; all expected/observed comparisons passed. I independently fetched all 57 unique transaction receipts from the Studionet RPC and retained each receipt's five validator votes, vote counts, round count, status, and consensus result in the machine-readable artifact. The observed vote splits include agree/idle and agree/disagree combinations as well as unanimous agreement. The earlier RPC errors were resolved by running network calls with authorized outbound access; failed attempts are not counted as scenario outcomes.

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

Machine-readable evidence is [`artifacts/studionet_live_evidence.json`](../artifacts/studionet_live_evidence.json). It contains 13 verified scenario records and RPC-read vote evidence for all 57 unique transactions, all on the same address. `gltest` clears the artifact directory on startup, so future runs must preserve and merge existing records before replacing this release artifact.
