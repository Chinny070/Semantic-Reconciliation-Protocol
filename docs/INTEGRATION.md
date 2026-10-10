# Integration guide

Consumers register an immutable order, a delivery record, and an invoice record, then call `reconcile(delivery_id, invoice_id)`. They should wait for transaction finality, read `get_reconciliation_certificate(id)`, read `get_reconciliation_state(id)`, and independently check `is_reconciliation_clear(id)` before acting. A consumer must not trust an intermediate receipt or prose; it should bind downstream logic to the order/policy hashes, evidence identities, and certificate hash. `MATCHED` is semantic reconciliation plus deterministic quantity checks; it is not bilateral acceptance, issuer authentication, payment approval, or settlement.

An authorized order participant can challenge a provisional receipt edge with `challenge_reconciliation(reconciliation_id, edge_hash, evidence_json)`. Each participant has one challenge during the bounded window. A sustained challenge creates a separate record available through `get_challenge`, voids provisional consumption after invariant checks, and leaves the original certificate auditable. `finalize_reconciliation` closes the window; finalized rights cannot be challenged. `EVIDENCE_UNAVAILABLE` is retryable up to three attempts for the same pair and never consumes quantity.

Use distinct deployments per test. The same contract serves procurement, construction, and logistics records through its JSON record interface. No web client or payment contract is required.

The interface and lifecycle behavior must be revalidated against current network tooling before consumer production use. Async cross-contract messaging is not part of v1.
