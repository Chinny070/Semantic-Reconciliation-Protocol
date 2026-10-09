# Correction lineage

Registered records are immutable. A correction names its predecessor and creates a successor pointer; a record with a successor is superseded and cannot be newly reconciled. Historical records remain readable. V1 does not reverse already finalized consumption; corrections that require reversal need an explicit future replay-safe reversal design.
