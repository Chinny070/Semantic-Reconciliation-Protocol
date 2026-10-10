# Cold and rejection-oriented steward audit

Audit target: source commit `948156b`, deployed to Studionet at `0x6cf5c63E9f5CddC9a113776Ea91b891907a90Fa7`. This is an internal adversarial review and does not claim an external steward's approval.

| Gate | Finding | Evidence and remaining boundary |
|---|---|---|
| Primitive and scope | PASS | One reusable order/delivery/invoice reconciliation contract; no frontend, ERP dashboard, payment, escrow, or marketplace. |
| GenLayer necessity | PASS | Validators classify semantic item/obligation relationships and public rendered evidence. Contract code owns all settlement arithmetic and state. See `DECISION.md`. |
| Semantic line-item graph | PASS with bounded allocation | Typed bounded edges and IDs are validated. A source line cannot feed multiple edges within one reconciliation; ambiguous split/many-to-many allocation fails closed. |
| Commercial obligation graph | PASS for implemented types | Frozen typed numeric/charge checks are deterministic; semantic document obligations return typed findings. Unsupported obligation forms reject at order creation. |
| Quantity/seman­tics boundary | PASS | Unit ratios are sealed with the order. Model output cannot set quantity, price, ratio, IDs, time, or state; exact arithmetic and capacity accounting are deterministic. Direct tests cover rational conversions, partial use, shortfall, overage, and price failures. |
| Substitution and hostile leader | PASS | Direct tests forge leader results, IDs, enums, decision fields, and errors. Live allowed, unauthorized, inferior, and ambiguous cases passed; prohibited or ambiguous outcomes consumed zero. |
| Duplicate ledger | PASS in verified live scope | Live disguised replay first consumed 10 then consumed zero on replay, records duplicate attempt/count, and leaves the second quantity ledger unchanged. |
| Corrections and recovery | PASS for declared v1 lifecycle | Delivery/invoice successors preserve lineage and supersede predecessors. Live invoice successor case passed. V1 does not reverse finalized consumption or amend orders. |
| Evidence retrieval/failure | PASS with bounded source model | Live HTTPS raw-GitHub evidence retrieval/rendering succeeded. Agreed source unavailability produced `EVIDENCE_UNAVAILABLE`, no edges, zero consumption, and no fraud accusation. Structured fixture content is submitter-provided. |
| Certificate, state, and validator evidence | PASS | Versioned portable certificates and quantity/state views were checked for all 15 scenarios. The evidence artifact retains the live transaction and readback records for the canonical address. |
| Runtime, schema and source parity | PASS | 74 Direct tests, GenVM lint, typecheck, 16-method schema validation, preflight, mutation checks, and deployed-source normalized hash were verified. Deployment finalized with `MAJORITY_AGREE`. |
| Novelty / collision | Defensible; not exhaustive | Decision record compares owner primitives and adjacent categories. No exhaustive portfolio, patent, or ecosystem-wide search is claimed. |
| Live matrix and release reproducibility | PASS | All 15 live scenarios were verified. Final evidence/docs are prepared for push, and a fresh clone passed the local gates plus on-chain schema retrieval. |

## Decision

The implementation has passed local validation, deployment/source parity, all required live scenarios, and final repository reproducibility checks. The candidate is frozen. The allocation, correction/reversal, and source-model limits are explicit v1 boundaries; this review is not an external steward approval.
