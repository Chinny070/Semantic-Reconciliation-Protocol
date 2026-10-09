# Cold and rejection-oriented audit

Audit performed against commit `2700b3970f9336499cfc11c7b4a3e9bc56c48e87`, after local tests and Studionet attempts. This is a findings record, not an approval.

## Rejection risks

| Gate | Finding | Evidence / required action |
|---|---|---|
| Primitive and scope | PASS | The implementation remains a standalone semantic order/delivery/invoice reconciliation contract; it adds no frontend, ERP, payment, escrow, or marketplace layer. |
| Deterministic settlement boundary | PASS with limits | Model output contains semantic edges and obligation statuses, while contract code derives quantities, unit conversions, prices, balances, IDs and receipt state. Frozen ratios prevent submitter-selected conversions. |
| Semantic line graph | PARTIAL | One-to-one source-line allocation is rejected when ambiguous. Safe grouped/many-to-one allocation is not implemented; the contract does not model split source allocation across separate edge groups. |
| Commercial obligation graph | PARTIAL / material | Obligation IDs and result enums are validated, but most obligation definitions remain prose and findings are model-returned PASS/FAIL. Exact threshold subtypes such as freight limits are not yet represented as typed deterministic fields and checked from invoice amounts. Do not claim all obligation types are enforceable. |
| Correction lineage | PARTIAL / material | Delivery and invoice successor links are immutable and supersede old records. Order amendments and deterministic consumption reversal/reissue are absent. |
| Evidence trust | PARTIAL | WEB_RENDERED requires HTTPS and invokes GenLayer rendering; validators independently retrieve and classify. Structured evidence remains writer-supplied content. Real web routes can fail and cause disagreement/reversion; the failure is fail-closed but not fully exposed as a distinct certificate outcome. |
| Validator equivalence | UNVERIFIED for latest code | The callback independently re-fetches and compares the full typed findings. Earlier deployment scenarios obtained majority agreement; the final packaging prompt clarification was not live-verified because Studionet became unreachable. Do not weaken equality to force agreement. |
| Arithmetic and ledger | PASS in tested paths | Direct tests cover integer conversions, partial source capacity, price ceilings, shortfall/overage, duplicate consumption, and unauthorized substitutions. Live semantic, partial and substitution cases passed on the preceding deployment. |
| Duplicate billing | PASS in prior live deployment | Directly queried certificate `R7` on `0xd9416b2ee3FFf48DcbafF598a1D4Ea68f8F0b272`: zero consumed quantity, `DUPLICATE_BILLING_ATTEMPT`, duplicate count 1, and `POSSIBLE_DUPLICATE_OF_PRIOR_LINE`. A later scenario also passed on `0x577627dc60776751bF4c5070144fe701ef6312C0`. Latest deployment still needs the full suite. |
| Source parity | UNVERIFIED for latest | A prior deployed source was byte-compared successfully. The latest code retrieval could not be performed after the RPC timed out. |
| Novelty / owner portfolio | INCOMPLETE | The fixed concept is distinct in its stated trust question, but no exhaustive owner-portfolio, ecosystem, repository, or patent search is claimed. |
| Submission evidence | INCOMPLETE | Latest address is deployed and finalized, but its live test set, source parity and Explorer verification are outstanding. |

## Decision

**Reject freeze and submission readiness for now.** The typed deterministic obligation gap is a contract-design gap. The final packaging behavior, latest-source parity, and latest-address live tests are blocked or unresolved. Resume from the latest commit and deployment in `docs/DEPLOYMENT.md`; do not label the candidate frozen until each applicable row is closed with evidence.
