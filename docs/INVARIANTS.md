# Protocol invariants

| ID | Invariant | Enforcement | Test/evidence |
|---|---|---|---|
| SR1 | Sealed order and policy are immutable. | `create_order` rejects duplicate ID; no update method. | `test_order_definition_is_immutable_and_duplicate_id_rejected` |
| SR2 | Semantic decisions and settlement arithmetic are separate. | Nondet functions return typed findings only; integer arithmetic follows consensus. | semantic match and packaging tests |
| SR3 | Quantity is conserved. | Positive source quantities; conversion ratios are frozen by the order; per-source remaining capacity and order remaining capacity cap consumption. | partial, split-capacity, overage, packaging tests |
| SR4 | Consumption cannot be replayed or exceed source/order capacity. | Pair replay guard plus consumed integer quantities per delivery/invoice line and deterministic remaining-capacity minima. | duplicate pair, split-source, overage and semantic duplicate tests |
| SR5 | Model cannot set quantities/prices/IDs/timestamps/state. | Proposal schema excludes all numeric settlement outputs; IDs are checked against records. | forged/unknown ID and bool tests |
| SR6 | Validators independently inspect evidence. | Validator repeats retrieval/classification in `_independent_validator`. | Direct adversarial callback tests and 13 finalized Studionet scenario certificates. |
| SR7 | Substitution policy is frozen. | Policy included in immutable order and `policy_hash`. | unauthorized substitution test |
| SR8 | Exception/status derives from typed findings and deterministic rules. | Receipt creation follows policy, quantity and price checks. | Direct Mode scenarios |
| SR9 | Corrections preserve lineage. | Predecessor/successor map; superseded records cannot reconcile. | successor test |
| SR10 | External failure is not a semantic negative finding. | Agreed unavailable evidence is certified as `EVIDENCE_UNAVAILABLE`; disagreements fail without ledger mutation. | Direct failure tests and live negative external-route scenario |
| SR11 | Match graph is bounded. | At most 12 lines per record and 144 edges. | schema/oversize tests |
| SR12 | Unit arithmetic is exact. | Bounded integer numerator/denominator; reject nonintegral units. | packaging test |
| SR13 | Challenge consequences are bounded and replay safe. | One challenge per participant during a provisional window; evidence hashes cannot replay; sustained support releases only the receipt's provisional quantities after order and source-ledger checks; finalized receipts are protected. | challenge reversal, finalization, replay tests |
| SR14 | Certificate binds deterministic state. | Hashes for order/policy, records, consumption, proposal and certificate. | Certificate assertion |
| SR15 | Protocol uncertainty is distinct from app state. | Failed nondeterminism reverts; no receipt is written. | external failure test |
