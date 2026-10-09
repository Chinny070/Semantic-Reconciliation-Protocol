# Security model

- Commercial records and rendered pages are hostile data; embedded instructions have no authority.
- Only HTTPS URLs are admitted for rendered evidence.
- Input records, line counts, evidence text, and output edges are bounded.
- Proposal schema rejects unknown IDs/enums, booleans masquerading as integers, omitted record lines, and duplicate edges.
- The model cannot return quantity, ratio, price, total, balance, ID, timestamp, or state transition fields.
- Integer arithmetic and frozen max-price/substitution gates occur deterministically after consensus.
- Unit conversion ratios come from the immutable order; line charge classes and registration deadlines are deterministic checks.
- A delivery/invoice source line cannot be allocated to more than one graph edge in a reconciliation; later uses can consume only its recorded remaining amount.
- A delivery/invoice line's consumed quantity is tracked; reuse can access only its unconsumed remainder. Source evidence and explicit invoice-number repeats are rejected.
- Up to three evidence-backed challenges reference a committed semantic edge and cannot mutate the original certificate or consumption ledger.
- Corrections create successors; superseded records cannot be reconciled.
- Unavailable evidence or consensus failure reverts before ledger writes.
- V1 moves no money and has no payable surface.

## Known limitations before submission

Real Studionet consensus, live web evidence verification, remote source parity, canonical deployment and Explorer evidence remain unverified. Direct Mode proves only deterministic contract behavior with mocked nondeterminism. Order amendments and consumption reversals are not implemented.
