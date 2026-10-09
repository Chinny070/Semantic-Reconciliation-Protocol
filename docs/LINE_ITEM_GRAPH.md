# Semantic Line-Item Graph

Each consensus edge binds one known order line, one delivery line, and one invoice line. The typed relation captures exact match, allowed equivalent, packaging equivalent, partial match, unauthorized/inferior substitution, unrelated, ambiguous, or insufficient evidence. IDs must already exist in the frozen records. Duplicate edge triples and omitted source lines are rejected. Quantities are intentionally absent from edge output.
