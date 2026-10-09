# Studionet live evidence ledger

This ledger preserves observed evidence from development deployments. The latest canonical deployment and its unverified gates are in [release verification](RELEASE_CANDIDATE_VERIFICATION.md). Results from older addresses do not prove behavior of the latest deployment.

## Historical development deployment `0xd9416b2ee3FFf48DcbafF598a1D4Ea68f8F0b272`

Deployment transaction `0x870a64c2748f02cd42a7ea642590baaa07de6b349707eeb1d39cbb540e4eeac3` was queried as `FINALIZED` with `MAJORITY_AGREE` and five votes. This deployment predates the per-order certificate view and the final packaging-prompt clarification.

| Scenario | Transaction hashes | Stored result observed |
|---|---|---|
| Rendered-evidence semantic match | `0x53b0720eac2d97dd778d8fbd0bb48c5f77e71910e232edd46bc5d126486b6808`; `0xcb913e87c0c5d5c62a209a77af9915e852d48bad0e83cd76e73b2895a14cb05f`; `0xbdfb0e1548c4af3c1b64d91714ac4f5ea6755c59ac174fef3c291793f70d5196`; `0x27679a0e57496279cdcbffd398bd951d4899db36e0c42a5c833de358d22cdf80` | `R1 MATCHED`, consumed 10 ordered units, no exceptions. Delivery and invoice evidence used `WEB_RENDERED` from the public fixture routes below. |
| Packaging/unit equivalence | `0xa1b6cf7b8a1683494525ad704310a5cce8bf47e52a6fcf2fbad628c9526b5231`; `0xae37f3b75239de8631d274debfc6281072bc7cd543fe3ec97061cca7fe71fdde`; `0x456e19a952a263eafb0d93197ce5de9ec358b99ca6e51055583a428425af71bb`; `0x421b351de0cecd13d747575c21860af86ee799090eac911087ca8a5aedb36651` | `R2 MATCHED`, consumed 24 units; semantic relation `PACKAGING_EQUIVALENT`; no exceptions. |
| Partial fulfillment | `0x775711b5166a6e657877220d0f6c80fbd9e9864e1f5f74977529c6fa206def5c`; `0x0018b9b488a4ba451937c3cf00e9fb0fbe04c2fb3d4e0eeef8b0aa5f9dffd59d`; `0x69f2dd0bfc3377ae58a9248fdc9c76f5c545611384ab07d460c636397c7124d7`; `0x4e25e86ba49eaef1aa0c8034e76f0d1c133ef7712ba68fcbe2a5dd2e433f413b` | `R3 PARTIAL_MATCH`, consumed 4 units from a 10-unit order. |
| Allowed equivalent substitution | `0x52b6e45da47cc58d014d231b8e76d54a583eb2e5e25a72cd9a601544fa2b3c1e`; `0xe6e971978f56539b1ee1e04d4798071380d0210b4909e3173cd98059a4e052ec`; `0x31f13717737123dd67eb4468d20abf71724ee2ea3cd8cf71ff2a2a7e9dc1b206`; `0x0a47d3b76a85ecfba92ceba748dcb3d9dbe1d3e710232dad4cfaaaf64cc2d788` | `R4 MATCHED`, consumed 10 units; edge and substitution were `ALLOWED_EQUIVALENT`. |
| Unauthorized substitution | `0x253c75e3ef0ae8df0026a3a98115f5115b1725b1324b3a29fa3c6646edf57a7e`; `0x52bb64222b39c2f2870ab23f63722abbd485e6f965e57740a544ec381ce239b0`; `0x9d201c986450d0b0b8576ccc8e250e5c706712402f3ef0fd7b8c3988673ddd8f`; `0x04d3c9354b815bdc531e01b6f7ece25579656f2a2dc70962a16c95ce096582ec` | `R5 INCONCLUSIVE`, consumed zero; exception `UNAUTHORIZED_SUBSTITUTION`. |
| Disguised duplicate invoice | Seven transactions finalized; the second reconciliation certificate was directly queried at `R7`. The test helper did not persist the transaction hashes in its artifact. | `R7 INCONCLUSIVE`, zero consumed, `DUPLICATE_BILLING_ATTEMPT`, duplicate count 1, semantic duplicate class `POSSIBLE_DUPLICATE_OF_PRIOR_LINE`. Certificate hash `64f82e9dc7fe6e460831961ea777c0a65fc3abaa5244ebd4c90db587350f6460`. |
| External evidence failure | `0x3e0a30a83a02cb6ae5225e11af571cbd29b4d8a1c5adb38d65a71d603711df7a`; `0x7bccc62688bd671a48f093b25165292856f58faf4934cb12d69225d9b30f7106`; `0x44aae043bd50fb979006b6ff6df7887f91d449c915de47adeb62328020ec3343`; `0xf157a50781c66df4ad91cbfb52c8404268f3ac5045fd0f67d6f0278251278b29` | Reconcile finalized `MAJORITY_DISAGREE`; remaining delivered/invoiced/reconciled quantities stayed zero. |

The public fixture URLs used for the rendered-evidence case were:

- `https://raw.githubusercontent.com/Chinny070/Semantic-Reconciliation-Protocol/main/fixtures/delivery/delivery-cement.json`
- `https://raw.githubusercontent.com/Chinny070/Semantic-Reconciliation-Protocol/main/fixtures/invoice/invoice-cement.json`

## Later deployment `0x577627dc60776751bF4c5070144fe701ef6312C0`

The full seven-case suite produced six passing scenario functions on this deployment: semantic match, partial fulfillment, allowed substitution, unauthorized substitution, disguised duplicate, and negative external-evidence failure. Packaging did not produce a latest certificate and was not counted as passing. The duplicate result was `R6 INCONCLUSIVE`, `DUPLICATE_BILLING_ATTEMPT`, zero consumed, with all seven scenario transactions finalized and majority-agreed.

## Latest deployment

Current canonical address `0xAa78272Caf6EAf7e523E78768319fBc2a65eF795` was deployed by `0x024a2bf6243324b76de4b7a1234a2a428402341f19ac625c9c28d6c6614b0821` from source commit `26b55af617c2a2844b44001fa49c4ea485596238`. Deployment finalized with `MAJORITY_AGREE` and schema contains 12 methods. Retrieved deployed source matches the committed local contract exactly after line-ending normalization; both SHA-256 values are `da277dea8a0db7f7cd94f5d6c592835ef06095aff7673de9ff2563ff0114f3ff`.

### Current-address integration run

Four scenarios passed with finalized `MAJORITY_AGREE` transactions and independently read certificates:

| Scenario | Certificate | Consumed quantity | Transaction hashes |
|---|---|---:|---|
| Rendered-evidence semantic match | `R3 MATCHED` | 10 | `0x2e20e82a96d9f4147d4353a8427ef23d3c78a44f531bb052a53bba7af8f1cf9d`; `0x5fd9cc2e50b6d286efdb4d07c213d3980ea378e8b7f22b5178d53ff8c9aba8ae`; `0xd5d153ab6c58571243b5233a10e41ebb3f6709b011f042b06280d0bb9ff07d88`; `0x5a5c2c13bbdb9c35cd9681672e2ccdfc0da5883f9f86ac1a1f91d96aa5986804` |
| Packaging/unit equivalence | `R4 MATCHED`, `PACKAGING_EQUIVALENT` | 24 | `0xa606fa8c4d6fb0a86018418985149f47fbfc7f27939db4c44dca11d916489817`; `0x0401cf1504c978f2ac13a81df5b963583d920edf713525180f99e7e7c61a08a7`; `0x8182a01fa5a41589b5d26e610fd91ac13cf1f9c26bf4d9850a107c2e2949d77a`; `0x6c78a0c6f4982161fa49c6d48837045dac980ad7bfc0865db8254d4981277bb0` |
| Partial fulfillment | `R5 PARTIAL_MATCH` | 4 | `0x762161e3d9897807c6b07321896c18d75b7830447d7bc046b0c07f0fbce6f955`; `0x371ec127aaab2dd6e2a3bebe7b557052feb50babd928fa0e41af40f9e9009852`; `0x1cfebbce611969cccf5f85031f61357ab4a57c3b6984284229414f98596e7202`; `0xef3859117767a2ed4285579b1e8219bb51a6a5ee5d869e31dc541f0be80f753d` |
| Permitted equivalent substitution | `R6 MATCHED`, `ALLOWED_EQUIVALENT` | 10 | `0xe940e2a712bea1322dbcfaac771971c07d9c4809147ace8f58e5c94f6b994298`; `0x422a3ce220c98f59db0d01fb387e5c053d00a18e0264edfc13a0e4b651ff3c43`; `0x340f272b3fbd2cd84488b2074fc8db688021d733740b0b3b6a2426975757f721`; `0x5d90055a11c8eb89efd9d5776a0c5f06fec1688424d20c9c5a7252c04578a590` |

Unauthorized substitution transaction `0x074dff0f3347ac148be92f7665672439a7a34961365bcc2b8576a43a9aaf2a2c` finalized `MAJORITY_DISAGREE` (three disagree votes, two idle). The stored output is fail-closed: zero consumed, `INCONCLUSIVE`, exception `UNAUTHORIZED_SUBSTITUTION`. Its edge is `ALLOWED_EQUIVALENT` / `ALLOWED_SUPERIOR` under `EXACT_REQUIRED`, so no ledger mutation occurred. This is recorded as a disagreement, not a consensus pass.

An isolated current-address duplicate run was verified earlier: seven finalized `MAJORITY_AGREE` transactions; `DUPLICATE_BILLING_ATTEMPT`, zero consumed, duplicate count 1, possible duplicate semantic class. In the full run the duplicate scenario later timed out during receipt polling, so that run is incomplete. The external-route failure test was retried once and again could not retrieve contract schema (`gltest` reported failure across default, hosted Studio, and local clients); no test transaction was submitted. A separate `genlayer trace` attempt returned RPC `Method not found` for `gen_dbg_traceTransaction`; the regular receipt was retrievable. The CLI-reported Explorer address page could not be accessed through the available browser lookup. Do not describe the complete seven-scenario suite or Explorer trail as verified.
