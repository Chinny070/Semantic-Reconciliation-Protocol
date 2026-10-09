# Implementation gap audit

Audit target: the initial workspace build before remediation, compared with `SEMANTIC_RECONCILIATION_PROTOCOL_CODEX_MASTER_PROMPT.md` and the user-supplied feature checklist. The table below is a historical baseline and must not be read as describing the current `26b55af` candidate. See the current-state re-audit below for what remains open.

| Requirement | Finding | Evidence and gap |
|---|---|---|
| Semantic Line-Item Graph | PARTIAL | Typed edges are bounded and IDs checked, but graph allocation does not safely support or reject ambiguous many-to-one allocation; multiple edges can overstate matching while only line IDs are locally deduplicated. |
| Commercial Obligation Graph | PARTIAL | Findings exist, but obligation definitions are mostly opaque prose; deadlines, location, documentation and fee limits have no typed deterministic representation or enforceable evidence rules. |
| Quantity–Semantics Separation | INCORRECT | The contract uses deterministic arithmetic, but accepts delivery/invoice ratios supplied by record submitters without binding them to a conversion policy frozen in the order. A caller can assert an arbitrary packaging ratio. |
| Substitution Policy Engine | INCORRECT | `NAMED_ALTERNATIVES_ONLY` compares the delivery description to an alternative with exact string equality; it does not bind the model's finding to a named alternative or enforce order-line identity consistently. Relation and substitution findings can contradict. |
| Partial Fulfillment | PARTIAL | A single line can be partially consumed, but source delivery/invoice lines are marked wholly used after partial consumption. This prevents valid remaining capacity from later reconciliation and leaves accepted delivered/invoiced totals capped rather than source-accurate. |
| Duplicate billing / consumption ledger | PARTIAL | Exact source hashes and whole-line replay guards exist. There is no independently identified invoice number (the record ID is hashed), no partial per-line capacity ledger, and semantic duplicate findings are not grounded in prior receipt identities. |
| Correction / successor lineage | PARTIAL | Delivery/invoice successors exist; lineage is not versioned as a full immutable graph, and duplicate evidence checks can prevent evidence-preserving corrected records. Order successor/amendment lineage is absent. |
| Evidence-backed challenge flow | MISSING | No challenge entry point, evidence binding, round bound, or challenge result exists. |
| Portable Reconciliation Certificate | PARTIAL | JSON certificate is available, but required matched delivery/invoice digests, exception attribution, external failure class, versioned schema, and source/evidence identity commitments are incomplete. |
| Deterministic quantity conservation | INCORRECT | Source line usage is boolean/whole-line, not a consumed amount. The code does not maintain all required per-source remaining quantities. |
| Deterministic unit/packaging arithmetic | INCORRECT | Integer rational arithmetic is used, but submitted ratios are untrusted and no frozen unit basis links them to the ordered unit. |
| Bounded state/history/graph behavior | INCORRECT | Per-record sizes/counts are bounded and orders/receipts capped, but delivery and invoice histories are unbounded. |
| Substantive GenLayer consensus | PARTIAL | Leader and validator classify semantic facts independently; structured fixture content is supplied by the writer rather than fetched or cryptographically anchored, and the semantic proposal can omit valid edge combinations without a sound allocation policy. |
| Independent validator re-evaluation | PARTIAL | A validator callback re-runs the observation/classification. Existing Direct Mode only checks a forged result with local mocked callbacks; live validator execution remains unverified. |
| Forged-leader resistance | PARTIAL | Schema and unequal typed outputs are rejected in a mock validator. Tests do not yet cover the required substantive wrong-but-well-formed classes and error wrappers comprehensively. |
| Evidence retrieval/rendering | PARTIAL | HTTPS rendering exists for `WEB_RENDERED`; redirects/host restrictions and structured/API evidence provenance are not verified. Live retrieval is untested. |
| External failure separation | PARTIAL | Exceptions fail closed by reverting; failures are not classified or exposed as a separate typed external-evidence outcome. |
| Prompt-injection resistance | PARTIAL | Prompt says evidence is untrusted, but no adversarial injection tests or extraction firewall prove records cannot override instructions. |
| Source/evidence identity | INCORRECT | Invoice number is derived from `record_id`; identity has no explicit issuer/reference fields, and normalized hashing can collapse records without validating their source lineage. |

## Current candidate residual audit (`26b55af`)

Verified improvements since the baseline include frozen order-defined rational unit conversions; partial quantity accounting for source lines; duplicate invoice identity and consumption checks; successor links for delivery/invoice corrections; versioned certificates with matched/remaining quantity and evidence digests; actual WEB_RENDERED retrieval and independent validator observations; and direct adversarial tests. Current live Studionet results are recorded in `LIVE_EVIDENCE.md`.

Still material: commercial obligation definitions remain predominantly prose with model-returned PASS/FAIL rather than typed deterministic threshold checks; order amendments and reversal/reissue of consumed quantities are not implemented; safe grouped/many-to-one source allocation is not implemented; unauthorized-substitution validator agreement failed to reach consensus on the latest deployed source; the full duplicate and external-route negative gates did not complete on the latest run due RPC availability; public Explorer verification remains outstanding. The candidate therefore remains not frozen.
| Downstream-friendly machine-readable views | PARTIAL | Certificate and remaining-quantity views exist, but there are no stable typed per-dimension/status views and certificate fields are incomplete. |
| No model-controlled settlement state | PARTIAL | Proposal schema excludes amounts and state. Deterministic logic still trusts caller-provided conversion ratios and permits cross-field semantic contradictions to affect consumption. |
| Scope discipline | COMPLETE | No frontend, ERP dashboard, payment, escrow, or marketplace layer was found. |
| Adversarial test matrix | MISSING | Current suite lacks required tests for deadline handling, unsupported charge, correction replay/capacity, prompt injection, external retrieval failures, over-consumption, malformed output/error classes, and certificate digest correctness. |
| Git / deployment / live proof | UNVERIFIED | Workspace has no `.git`; earlier attempts reported host-denied GitHub and Studionet connectivity. Must retry after local remediation. |

This report records the pre-remediation audit. Material fixes and unresolved gaps are tracked below.

## Remediation update

The contract now freezes unit conversions in the order, records source-line consumption amounts, caps delivery/invoice history, requires an explicit invoice number and public counterparty address, binds line charge class and registration deadline, rejects one source line allocated to multiple edges, emits complete quantity/edge/exception/evidence digests, and supports up to three evidence-backed challenge rounds without rewriting the original receipt. Prior consumed invoice lines and evidence hashes go to both leader and validator for disguised-duplicate analysis. Tests cover these changes, prompt data framing, malformed output, invalid HTTPS routing, quantity shortfall/overage, and superior-substitution policy.

Remediation completed after this historical baseline: arbitrary submitter unit ratios were removed; source quantity consumption is tracked per line; delivery/invoice histories are bounded; invoice numbers and counterparties are explicit; duplicate history is supplied to both leader and validator; evidence challenges and portable digest fields were added; a GenVM runtime failure caused by non-persistent Python counters was corrected with declared storage; and a per-order latest-certificate view was added. The validator prompt now distinguishes packaging relation from same-unit equivalent wording.

Current unresolved gaps are recorded in [the cold rejection audit](STEWARD_REJECTION_AUDIT.md). In particular, typed deterministic enforcement of numeric Commercial Obligation Graph thresholds, order amendment/reversal lineage, latest-deployment live scenario completion, latest-source parity, Explorer proof, clean-clone verification, and exhaustive novelty review remain incomplete. This gap report does not authorize freeze.
