# Duplicate billing and consumption

The exact layer rejects repeated record IDs, explicit invoice numbers, and duplicate evidence content. The semantic layer classifies possible disguised duplicates/same underlying charges; any result other than `DISTINCT_CHARGE` cannot consume capacity. Deterministic per-source remaining quantities remain authoritative: a partially used line can be consumed only for its unconsumed remainder, while a reworded charge cannot reuse already consumed order capacity.
