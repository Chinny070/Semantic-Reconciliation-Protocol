# Consensus design

## Nondeterministic operations

`gl.nondet.web.render(url, mode="text")` is used for records explicitly registered as `WEB_RENDERED`. `gl.nondet.exec_prompt(prompt, response_format="json")` returns the bounded semantic proposal. Structured fixtures/API/public documents are supplied as immutable committed content and are not presented as independently retrieved web observations.

## Leader and validators

The leader loads frozen order/policy and record evidence, retrieves each web source once, then asks for IDs and typed semantic classes only. It explicitly frames all records/evidence as one JSON-escaped untrusted data object and tells the classifier to ignore embedded instructions. It prohibits quantity, ratio, price and balance derivation.

The validator validates the leader schema, independently performs the same retrieval and semantic classification, then compares evidence sufficiency, obligation findings, edge IDs/relation/substitution/duplicate classes, unmatched graph nodes, and the complete observed evidence identities (retrieval kind, source, bounded-content digest, provenance class). It rejects malformed/exceptional leaders and any mismatch. Direct Mode skips real validator consensus; only a live Studionet run can prove this path.

## Failure and equivalence

Unknown enums, omitted lines, unknown IDs, duplicate edges, malformed JSON, unsupported obligation results, unavailable evidence, and disagreement fail closed. Rationale prose is absent from the consensus payload; only stable typed decision fields are compared.

## Load-bearing role

Without GenLayer, a single trusted operator must decide whether differently worded goods/services/charges correspond. The contract cannot infer that fact deterministically from prose. Validator independence reduces reliance on one supplier, buyer, OCR service, or leader model. Deterministic code then limits exactly what agreement can consume.
