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

- **Semantic Line-Item Graph:** bounded order/delivery/invoice edges with typed relation and substitution classes.
- **Commercial Obligation Graph:** frozen semantic obligations whose findings are checked after consensus.
- **Quantity–Semantics Separation:** bounded unit conversions are frozen in the order; record submitters cannot supply ratios, and multiplication/divisibility/consumption happen in deterministic code.
- **Substitution Policy Engine:** policy is frozen in the order and constrains the accepted semantic substitution class.
- **Partial fulfillment:** consumption records remaining order capacity across receipts.
- **Duplicate prevention:** invoice-number/content identity and semantic prior-charge findings block reuse; per-source remaining quantities permit valid partial consumption without double use.
- **Correction lineage:** delivery and invoice successors preserve old records and supersede them for future reconciliation.
- **Evidence-backed challenges:** up to three new-evidence findings can challenge a receipt edge; a challenge cannot rewrite the receipt or quantity ledger.
- **Portable certificate:** stored JSON view binds order, policy, record/evidence roots, semantic edges, deterministic consumption, quantity digests, exceptions, and consensus output.
- **Bounded state:** at most 64 orders, 64 deliveries, 64 invoices and 64 receipts; record lines and evidence sizes are also bounded.

## Run local checks

Use Python 3.12 and the pinned packages in `requirements-test.txt`.

```powershell
$env:PYTHONIOENCODING='utf-8'
gltest tests/direct -v -s
genvm-lint check contracts/semantic_reconciliation.py --json
genvm-lint typecheck contracts/semantic_reconciliation.py
python scripts/preflight.py
```

Direct Mode mocks only nondeterminism; it is not proof of real validator consensus. Integration testing on Studionet is separate and requires network access. Current deployment and live evidence are recorded in `docs/RELEASE_CANDIDATE_VERIFICATION.md` only after they are observed.

## Reusable consumers

Wholesale procurement consumes purchase-order/warehouse/invoice certificates; construction consumes bill-of-quantities/site-delivery/contractor-invoice certificates; logistics consumes shipping-order/proof-of-delivery/carrier-invoice certificates. None needs its own semantic matching model.

See [architecture](docs/ARCHITECTURE.md), [consensus](docs/CONSENSUS.md), [security](docs/SECURITY.md), and [integration](docs/INTEGRATION.md).
