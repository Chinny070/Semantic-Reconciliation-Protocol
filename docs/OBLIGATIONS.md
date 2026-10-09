# Commercial Obligation Graph

Orders carry at most 12 typed obligations. Every obligation contains `obligation_id`, `type`, `definition`, `evaluation_mode`, `criticality`, and a bounded type-specific `parameters` object. IDs are unique and frozen with the order. The model receives only SEMANTIC obligations; it returns one of `PASS`, `FAIL`, `AMBIGUOUS`, or `INSUFFICIENT_EVIDENCE` for each semantic ID. Missing/extra IDs and unknown findings fail closed. Deterministic obligations are not model outputs: the contract derives their result and includes it in the certificate.

Supported deterministic forms are:

- `DELIVERY_DEADLINE`: `parameters.deadline_timestamp`; compares the immutable delivery registration timestamp with the frozen Unix timestamp. This is a registration deadline, not a claim about the physical handoff time.
- `MAX_UNIT_PRICE`: `parameters.order_line_id` and `maximum_unit_price_minor`; must tighten the referenced order line's existing ceiling. Invoice unit prices are normalized against the order-frozen integer unit ratio before comparison.
- `MAX_FREIGHT_CHARGE`: `parameters.maximum_amount_minor`; sums `quantity × unit_price_minor` for invoice lines whose frozen class is exactly `FREIGHT`, then compares the integer total to the cap.
- `NO_EXTRA_SURCHARGE`: `parameters.permitted_charge_classes`; every invoice line's class must occur in the frozen list.

The existing line-level `deadline_timestamp`, `max_unit_price_minor`, and exact `charge_class` checks remain deterministic safeguards. These obligations do not rely on model arithmetic.

Semantic forms include delivery location, required certificate, serial-number list, inspection, and service milestone requirements. The model may judge whether evidence semantically satisfies them, but cannot alter quantities, timestamps, or numeric limits. A non-PASS obligation prevents quantity consumption and appears in the portable certificate. Unknown/unimplemented obligation types are rejected at order creation; free-form prose is never interpreted as an arithmetic threshold.
