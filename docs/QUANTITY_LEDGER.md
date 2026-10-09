# Quantity ledger

Each order line freezes its unit-conversion table before fulfillment. A conversion is a positive bounded rational number of canonical order units per declared source unit; the ordered unit must map to exactly one. Delivery and invoice records provide a unit label and integer quantity only. They cannot provide or change conversion ratios.

The contract multiplies by the frozen numerator, checks divisibility by the denominator, and computes the available amount as the minimum of remaining delivery capacity, remaining invoice capacity, and remaining order capacity. It stores consumed amounts per source record line, so an unconsumed remainder may be paired with a later invoice or delivery. It never consumes the same source capacity twice.

If delivery and invoice quantities differ, or exceed the remaining ordered quantity, the certificate records a quantity exception and caps consumption. A deterministic price ceiling is normalized using the same frozen unit conversion. Floats and model-generated quantities are unsupported.
