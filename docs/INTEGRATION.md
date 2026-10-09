# Integration guide

Consumers register an immutable order, a delivery record, and an invoice record, then call `reconcile(delivery_id, invoice_id)`. They should wait for transaction finality, read `get_reconciliation_certificate(id)`, and independently check `is_reconciliation_clear(id)` before acting. A consumer must not trust an intermediate receipt or prose; it should bind downstream logic to the order/policy hashes and certificate hash.

An authorized order participant can challenge a receipt edge with `challenge_reconciliation(reconciliation_id, edge_hash, evidence_json)`. The challenge result is a separate bounded record available through `get_challenge`; it never reverses consumption or rewrites the original certificate. Delivery registration timestamps are chain transaction times, and are used conservatively against any frozen line deadline.

Use distinct deployments per test. The same contract serves procurement, construction, and logistics records through its JSON record interface. No web client or payment contract is required.

The interface and lifecycle behavior must be revalidated against current network tooling before consumer production use. Async cross-contract messaging is not part of v1.
