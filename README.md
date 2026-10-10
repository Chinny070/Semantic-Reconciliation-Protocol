# Semantic Reconciliation Protocol

**Consensus-backed three-way matching for purchase orders, delivery records, and invoices.**

The protocol answers whether differently worded commercial records refer to the same goods or obligation. GenLayer validators independently inspect the evidence and classify bounded semantic edges. Deterministic contract logic applies frozen substitution policy, exact unit ratios, quantity limits, price ceilings, and duplicate-consumption rules. The result is a portable certificate; this contract does not move money.

```text
Frozen order + policy
        ↓
delivery record(s) + invoice(s)
        ↓
independent semantic edge findings (GenLayer)
        ↓
deterministic units, price, consumption and exceptions
        ↓
portable reconciliation certificate
```

## What is implemented

- **Semantic Line-Item Graph:** bounded order/delivery/invoice edges with typed relation and substitution classes, plus explicit unmatched nodes for undelivered orders, unbilled deliveries, unsupported invoices, unrelated lines, and ambiguity. No source ID is fabricated.
- **Commercial Obligation Graph:** bounded typed obligations include deterministic delivery deadlines, unit-price ceilings, maximum freight totals, and permitted charge classes, plus semantic location, certificate, serial, inspection, and service-milestone findings. Deterministic values are checked in contract code; the model does not calculate or decide numeric limits.
- **Quantity–Semantics Separation:** bounded unit conversions are frozen in the order; record submitters cannot supply ratios, and multiplication/divisibility/consumption happen in deterministic code.
- **Substitution Policy Engine:** policy is frozen in the order and constrains the accepted semantic substitution class.
- **Partial fulfillment:** consumption records remaining order capacity across receipts.
- **Duplicate prevention:** invoice-number/content identity and semantic prior-charge findings block reuse; per-source remaining quantities permit valid partial consumption without double use.
- **Correction lineage:** immutable delivery and invoice successors preserve readable historical records and supersede predecessors for future reconciliation. Successors are registrar-bound and invoice identity is order-scoped.
- **Evidence failure:** when validators agree that a required external source is unavailable, the contract stores an `EVIDENCE_UNAVAILABLE` certificate with no semantic edges and no consumption. A source disagreement fails without state advance and is not treated as fraud or a mismatch.
- **Evidence-backed challenges:** each participant has one bounded challenge during a provisional receipt's challenge window. A sustained challenge voids provisional consumption with invariant checks; finalized receipts cannot be challenged. The original certificate remains auditable.
- **Portable certificate:** stored JSON view binds order, policy, record/evidence roots, semantic edges, deterministic consumption, quantity digests, exceptions, and consensus output.
- **Bounded state:** records and receipts are capped per order, and orders are capped per creator, so one participant cannot consume another order's lifetime capacity. Record lines, evidence, prior-charge context, and graph size are bounded.

## Run local checks

Use Python 3.12 and the exact packages in `requirements-lock.txt`.

```powershell
$env:PYTHONUTF8='1'
python -m pytest tests/direct -q
genvm-lint check contracts/semantic_reconciliation.py --json
genvm-lint typecheck contracts/semantic_reconciliation.py
python scripts/preflight.py
```

Direct Mode mocks only nondeterminism; it is not proof of real validator consensus. Integration testing on Studionet is separate and requires network access. Current deployment and live evidence are recorded in `docs/RELEASE_CANDIDATE_VERIFICATION.md` only after they are observed.

## Release status

The current release evidence is recorded only after the corrected deployment and live matrix are independently verified. See [live evidence](docs/LIVE_EVIDENCE.md), [deployment](docs/DEPLOYMENT.md), and [release verification](docs/RELEASE_CANDIDATE_VERIFICATION.md). The protocol does not move money or assert issuer authenticity or bilateral commercial acceptance.

## Reusable consumers

Wholesale procurement consumes purchase-order/warehouse/invoice certificates; construction consumes bill-of-quantities/site-delivery/contractor-invoice certificates; logistics consumes shipping-order/proof-of-delivery/carrier-invoice certificates. None needs its own semantic matching model.

See [architecture](docs/ARCHITECTURE.md), [consensus](docs/CONSENSUS.md), [security](docs/SECURITY.md), and [integration](docs/INTEGRATION.md).
