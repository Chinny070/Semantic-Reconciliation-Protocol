# Architecture and protocol specification

## Primitive and trust boundary

The protocol semantically relates one sealed order to bounded delivery and invoice records. Its Semantic Line-Item Graph contains typed order/delivery/invoice edges. Its Commercial Obligation Graph records frozen non-line-item requirements. GenLayer classifies semantic identity, equivalence, substitution, duplicate-charge relation, and semantic obligation satisfaction. The contract validates IDs/enums and deterministically owns all numeric and state effects.

## Bounded records

One order has 1–12 lines and 0–12 obligations. Each delivery or invoice has 1–12 lines and bounded source/evidence strings. Integer quantities are positive bounded integers. Rational unit conversions live only in the sealed order; delivery/invoice records cannot choose ratios. Invoice unit prices use integer minor currency units and charge classes must match the frozen order line. Evidence retrieval kinds are `STRUCTURED_FIXTURE`, `API_JSON`, `PUBLIC_DOCUMENT`, and `WEB_RENDERED`. Delivery/invoice histories are each capped at 64; a delivery registration timestamp is captured from GenVM's deterministic transaction clock. A sealed record is immutable; corrections register successors.

## Reconciliation

1. Freeze order and substitution policy hashes.
2. Register delivery and invoice definitions with evidence sources.
3. Leader retrieves each source once, classifies typed edges, substitutions, duplicates and obligations.
4. Each validator independently repeats observation/classification and compares every decision-critical field.
5. Deterministic code validates the returned proposal, policy and obligations; normalizes only by registered integer ratios; applies remaining capacities and max prices; then writes a receipt/certificate.

No storage mutation occurs inside nondeterministic functions. Any unavailable source, malformed proposal, disagreement or insufficient evidence reverts; it is not finalized as breach.

## Limits and intentionally unimplemented scope

The contract supports bounded one-to-one source-line allocation, split consumption of remaining line capacity, typed obligation findings, and up to three evidence-backed challenge findings per receipt. Challenges do not rewrite or reverse receipts. It does not implement payments, frontends, fee settlement, order amendments, consumption reversals, nor multi-line grouped allocation. Certificates are stored as canonical JSON and exposed by view. This is not submission-ready until every deterministic obligation subtype is specified, live validation and source parity pass, and the remote release gates are completed.
