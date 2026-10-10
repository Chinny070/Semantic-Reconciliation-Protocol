# Architecture and protocol specification

## Primitive and trust boundary

The protocol semantically relates one sealed order to bounded delivery and invoice records. Its Semantic Line-Item Graph contains typed order/delivery/invoice edges. Its Commercial Obligation Graph records frozen non-line-item requirements. GenLayer classifies semantic identity, equivalence, substitution, duplicate-charge relation, and semantic obligation satisfaction. The contract validates IDs/enums and deterministically owns all numeric and state effects.

## Bounded records

One order has 1–12 lines and 0–12 obligations. Each delivery or invoice has 1–12 lines and bounded source/evidence strings. Integer quantities are positive bounded integers. Rational unit conversions live only in the sealed order; delivery/invoice records cannot choose ratios. Invoice unit prices use integer minor currency units and charge classes must match the frozen order line. Supported evidence retrieval kinds are `STRUCTURED_FIXTURE` and `WEB_RENDERED`; unsupported kinds fail closed. Delivery/invoice histories are capped per order and orders per creator. A sealed record is immutable; corrections register successors owned by the original registrar.

## Reconciliation

1. Freeze order and substitution policy hashes.
2. Register delivery and invoice definitions with evidence sources.
3. Leader retrieves each source once, classifies typed edges, semantic substitution classes, duplicates and semantic obligations.
4. Each validator independently repeats observation/classification and compares decision-critical IDs, relation/substitution/duplicate enums, unmatched graph nodes, semantic obligation results, evidence sufficiency, and the observed evidence identity: retrieval kind, exact source, bounded-content digest, and provenance class. Prose and confidence are not part of the decision schema.
5. Deterministic code validates the returned proposal, applies the frozen substitution policy, evaluates typed numeric obligations, normalizes only by registered integer ratios, applies remaining capacities and price ceilings, then writes a receipt/certificate.

No storage mutation occurs inside nondeterministic functions. If external retrieval is unavailable and the independent validators agree on that result, the contract stores an `EVIDENCE_UNAVAILABLE` certificate with no semantic edges and no quantity consumption. If validators see different evidence or disagree on decision-critical findings, the transaction fails closed without state advance; that disagreement is not a commercial accusation.

## Limits and intentionally unimplemented scope

The contract supports bounded source-line allocation, split consumption of remaining line capacity across records, explicit unmatched graph nodes, typed semantic and deterministic obligations, immutable delivery/invoice successors with record-read views, retryable evidence-unavailable attempts, and provisional challengeable receipts. A sustained challenge releases provisional quantities only after checking every affected order and source ledger invariant. Finalization protects legitimate rights; historical certificates remain unchanged. The contract does not implement issuer authentication, bilateral acceptance, payments, frontends, or fee settlement. Certificates are stored as canonical JSON and exposed by view.
