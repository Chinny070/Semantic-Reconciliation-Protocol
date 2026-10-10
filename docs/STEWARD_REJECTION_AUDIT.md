# Cold and rejection-oriented steward audit

Audit target: source commit `3c507a8eb875d8988ce8c14962eafd003fb2e195`, deployed to Studionet at `0xEdcdC09588C71aDD0B10396A07Bb022a4a3b3D56`. This is an internal adversarial review and does not claim an external steward's approval.

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
| Certificate and state | PASS | Versioned portable certificate binds record, policy, evidence, edge, quantity, and exception digests. Stored certificates and quantity views were checked for all 13 recorded scenarios. |
| Runtime, schema and source parity | PASS | 52 Direct tests, GenVM lint, typecheck, 14-method schema validation, preflight, and deployed-source normalized hash were verified. Deployment finalized with `MAJORITY_AGREE`; Explorer showed finality and accepted deployment. |
| Novelty / collision | Defensible; not exhaustive | Decision record compares owner primitives and adjacent categories. No exhaustive portfolio, patent, or ecosystem-wide search is claimed. |
| Live matrix and release reproducibility | Live matrix PASS; repository gates pending | All 13 live scenarios have verified expected results with finalized `MAJORITY_AGREE` receipts. Final docs/evidence push, clean clone, and clean worktree checks remain. |

## Decision

The implementation has passed the local validation gates, deployment/source parity, and all required live scenarios. Freeze only after the final evidence/docs commit is pushed and the clean-clone and clean-worktree checks pass. The allocation, correction/reversal, and source-model limits are explicit v1 boundaries.
