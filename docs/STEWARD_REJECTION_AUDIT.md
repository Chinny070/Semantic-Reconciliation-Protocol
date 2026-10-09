# Cold and rejection-oriented audit

Audit performed against source commit `26b55af617c2a2844b44001fa49c4ea485596238`, after local tests and current-address Studionet attempts. This is a findings record, not an approval.

## Rejection risks

| Gate | Finding | Evidence / required action |
|---|---|---|
| Primitive and scope | PASS | The implementation remains a standalone semantic order/delivery/invoice reconciliation contract; it adds no frontend, ERP, payment, escrow, or marketplace layer. |
| Deterministic settlement boundary | PASS with limits | Model output contains semantic edges and obligation statuses, while contract code derives quantities, unit conversions, prices, balances, IDs and receipt state. Frozen ratios prevent submitter-selected conversions. |
| Semantic line graph | PARTIAL | One-to-one source-line allocation is rejected when ambiguous. Safe grouped/many-to-one allocation is not implemented; the contract does not model split source allocation across separate edge groups. |
| Commercial obligation graph | PARTIAL / material | Obligation IDs and result enums are validated, but most obligation definitions remain prose and findings are model-returned PASS/FAIL. Exact threshold subtypes such as freight limits are not yet represented as typed deterministic fields and checked from invoice amounts. Do not claim all obligation types are enforceable. |
| Correction lineage | PARTIAL / material | Delivery and invoice successor links are immutable and supersede old records. Order amendments and deterministic consumption reversal/reissue are absent. |
| Evidence trust | PARTIAL | WEB_RENDERED requires HTTPS and invokes GenLayer rendering; validators independently retrieve and classify. Structured evidence remains writer-supplied content. Real web routes can fail and cause disagreement/reversion; the failure is fail-closed but not fully exposed as a distinct certificate outcome. |
| Validator equivalence | PARTIAL / material | Current-address semantic, packaging, partial, and permitted-equivalent scenarios finalized with majority agreement. Unauthorized substitution produced `MAJORITY_DISAGREE`; the leader receipt shows a valid fail-closed `INCONCLUSIVE` certificate with zero consumption and `UNAUTHORIZED_SUBSTITUTION`, but it did not reach agreed validator output. Do not weaken equality to force agreement. |
| Arithmetic and ledger | PASS in tested paths | Direct tests cover integer conversions, partial source capacity, price ceilings, shortfall/overage, duplicate consumption, and unauthorized substitutions. Live semantic, partial and substitution cases passed on the preceding deployment. |
| Duplicate billing | PASS isolated; full-run incomplete | An isolated run on current address `0xAa78272Caf6EAf7e523E78768319fBc2a65eF795` produced seven finalized majority-agreed transactions and a certificate with zero consumption, `DUPLICATE_BILLING_ATTEMPT`, count 1, and `POSSIBLE_DUPLICATE_OF_PRIOR_LINE`. The full suite later timed out while polling its duplicate scenario. |
| Source parity | PASS | Retrieved deployed source for `0xAa78272Caf6EAf7e523E78768319fBc2a65eF795`; normalized text exactly equals local contract source. Both SHA-256 values are `da277dea8a0db7f7cd94f5d6c592835ef06095aff7673de9ff2563ff0114f3ff`. |
| Novelty / owner portfolio | INCOMPLETE | The fixed concept is distinct in its stated trust question, but no exhaustive owner-portfolio, ecosystem, repository, or patent search is claimed. |
| Submission evidence | INCOMPLETE | Latest address is deployed and finalized. Four current-address scenarios passed; unauthorized reached fail-closed disagreement; duplicate polling timed out; external-route failure setup could not retrieve schema. Explorer proof is outstanding. |

## Decision

**Reject freeze and submission readiness for now.** Typed deterministic obligation enforcement and order amendment/reversal remain material design gaps. Current-address source parity and four live semantic cases are verified, while unauthorized validator agreement, full-run duplicate and external-route failure remain unresolved; Explorer proof is outstanding. Resume from the latest commit and deployment in `docs/DEPLOYMENT.md`; do not label the candidate frozen until each applicable row is closed with evidence.
