# Security model

- Commercial records and rendered pages are hostile data; embedded instructions have no authority.
- Only HTTPS URLs are admitted for rendered evidence.
- Input records, line counts, evidence text, and output edges are bounded.
- Proposal schema rejects unknown IDs/enums, booleans masquerading as integers, omitted record lines, duplicate edges, and lines represented both as matched and unmatched. Unmatched nodes explicitly preserve partial and unequal line sets.
- The model cannot return quantity, ratio, price, total, balance, ID, timestamp, or state transition fields.
- Integer arithmetic and frozen max-price/substitution gates occur deterministically after consensus.
- Unit conversion ratios come from the immutable order; line charge classes and registration deadlines are deterministic checks.
- A delivery/invoice source line cannot be allocated to more than one graph edge in a reconciliation; later uses can consume only its recorded remaining amount.
- A delivery/invoice line's consumed quantity is tracked; reuse can access only its unconsumed remainder. Source evidence and explicit invoice-number repeats are rejected.
- Provisional evidence-backed challenges are one per participant per receipt, replay protected, and window bounded. A sustained challenge releases provisional consumption only after checking order, delivery, and invoice ledger invariants; finalized receipts are protected.
- Corrections create successors; superseded records cannot be reconciled.
- Unavailable evidence writes a zero-consumption retryable record; consensus disagreement reverts before ledger writes. A definitive semantic result consumes the pair exactly once.
- `registered_by` is only the on-chain registrar. It does not authenticate an external issuer or prove counterparty assent. `WEB_RENDERED` is an independently observed page and its digest is bound into validator equivalence; HTTPS alone is not commercial provenance.
- V1 moves no money and has no payable surface.

## Known limitations before submission

Direct Mode proves deterministic behavior with mocked nondeterminism; the separate canonical Studionet matrix records live validator consensus and rendered evidence. Deployment finality, source parity and Explorer status are recorded in `DEPLOYMENT.md`. V1 does not amend orders or reverse finalized consumption. Ambiguous split allocation is rejected rather than guessed. Structured fixture content is still writer-supplied; only registered rendered URLs are fetched independently.
