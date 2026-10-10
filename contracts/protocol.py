"""Pure bounded schema and deterministic policy helpers for the protocol."""
import json

MAX_LINES = 12
MAX_OBLIGATIONS = 12
MAX_RECORD_BYTES = 12000
MAX_EVIDENCE_BYTES = 24000
MAX_OUTPUT_BYTES = 12000
MAX_HISTORY = 64
MAX_DELIVERY_RECORDS = 64
MAX_INVOICE_RECORDS = 64
MAX_RATIO = 1000000
RELATIONS = (
    "EXACT_MATCH", "ALLOWED_EQUIVALENT", "PACKAGING_EQUIVALENT", "PARTIAL_MATCH",
    "UNAUTHORIZED_SUBSTITUTION", "INFERIOR_SUBSTITUTION", "UNRELATED", "AMBIGUOUS",
    "INSUFFICIENT_EVIDENCE",
)
SUBSTITUTIONS = (
    "EXACT", "ALLOWED_EQUIVALENT", "ALLOWED_SUPERIOR", "UNAUTHORIZED_SUBSTITUTE",
    "INFERIOR_SUBSTITUTE", "AMBIGUOUS",
)
POLICIES = (
    "EXACT_REQUIRED", "EQUIVALENT_ALLOWED", "SUPERIOR_ALLOWED", "NAMED_ALTERNATIVES_ONLY",
    "NO_SUBSTITUTION",
)
OBLIGATION_TYPES = (
    "DELIVERY_DEADLINE", "MAX_UNIT_PRICE", "MAX_FREIGHT_CHARGE", "NO_EXTRA_SURCHARGE",
    "DELIVERY_LOCATION", "REQUIRED_CERTIFICATE", "SERIAL_NUMBER_LIST", "INSPECTION_REQUIRED",
    "SERVICE_MILESTONE",
)
DETERMINISTIC_OBLIGATIONS = {
    "DELIVERY_DEADLINE", "MAX_UNIT_PRICE", "MAX_FREIGHT_CHARGE", "NO_EXTRA_SURCHARGE",
}


def _bounded_text(value, field, limit=512):
    if not isinstance(value, str) or not value or len(value) > limit:
        raise ValueError("invalid " + field)
    return value


def _integer(value, field, maximum=2**63 - 1):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > maximum:
        raise ValueError("invalid " + field)
    return value


def _positive(value, field, maximum=2**63 - 1):
    result = _integer(value, field, maximum)
    if result == 0:
        raise ValueError(field + " must be positive")
    return result


def _parse_object(raw, field, max_bytes=MAX_RECORD_BYTES):
    if not isinstance(raw, str) or len(raw.encode("utf-8")) > max_bytes:
        raise ValueError(field + " too large")
    try:
        parsed = json.loads(raw)
    except Exception:
        raise ValueError("invalid " + field + " JSON")
    if not isinstance(parsed, dict):
        raise ValueError(field + " must be an object")
    return parsed


def validate_order(raw):
    order = _parse_object(raw, "order")
    if set(order) != {"order_id", "counterparty", "lines", "obligations"}:
        raise ValueError("unexpected or missing order fields")
    _bounded_text(order["order_id"], "order_id", 96)
    _bounded_text(order["counterparty"], "counterparty", 160)
    if (len(order["counterparty"]) != 42 or not order["counterparty"].startswith("0x")
            or any(ch not in "0123456789abcdefABCDEF" for ch in order["counterparty"][2:])):
        raise ValueError("counterparty must be a public account address")
    order["counterparty"] = order["counterparty"].lower()
    lines, obligations = order["lines"], order["obligations"]
    if not isinstance(lines, list) or not 1 <= len(lines) <= MAX_LINES:
        raise ValueError("line count out of bounds")
    if not isinstance(obligations, list) or len(obligations) > MAX_OBLIGATIONS:
        raise ValueError("obligation count out of bounds")
    ids = set()
    for line in lines:
        if not isinstance(line, dict) or set(line) != {
            "line_id", "description", "unit", "quantity", "max_unit_price_minor", "charge_class", "deadline_timestamp",
            "unit_conversions", "substitution_policy", "named_alternatives", "criticality",
        }:
            raise ValueError("invalid order line fields")
        lid = _bounded_text(line["line_id"], "line_id", 96)
        if lid in ids:
            raise ValueError("duplicate order line id")
        ids.add(lid)
        _bounded_text(line["description"], "line description")
        _bounded_text(line["unit"], "line unit", 64)
        _positive(line["quantity"], "ordered quantity")
        _integer(line["max_unit_price_minor"], "maximum unit price")
        _bounded_text(line["charge_class"], "ordered charge class", 64)
        _integer(line["deadline_timestamp"], "deadline timestamp")
        conversions = line["unit_conversions"]
        if not isinstance(conversions, list) or not 1 <= len(conversions) <= 8:
            raise ValueError("invalid frozen unit conversions")
        conversion_units = set()
        for conversion in conversions:
            if not isinstance(conversion, dict) or set(conversion) != {"unit", "numerator", "denominator"}:
                raise ValueError("invalid frozen unit conversion")
            unit = _bounded_text(conversion["unit"], "conversion unit", 64)
            if unit in conversion_units:
                raise ValueError("duplicate conversion unit")
            conversion_units.add(unit)
            _positive(conversion["numerator"], "conversion numerator", MAX_RATIO)
            _positive(conversion["denominator"], "conversion denominator", MAX_RATIO)
        if line["unit"] not in conversion_units:
            raise ValueError("ordered unit must have a frozen conversion")
        if not any(x["unit"] == line["unit"] and x["numerator"] == x["denominator"] for x in conversions):
            raise ValueError("ordered unit conversion must equal one")
        if line["substitution_policy"] not in POLICIES:
            raise ValueError("unknown substitution policy")
        alts = line["named_alternatives"]
        if not isinstance(alts, list) or len(alts) > 8:
            raise ValueError("invalid named alternatives")
        for alt in alts:
            _bounded_text(alt, "named alternative", 160)
        if line["criticality"] not in ("CRITICAL", "STANDARD"):
            raise ValueError("invalid criticality")
    obligation_ids = set()
    for item in obligations:
        if not isinstance(item, dict) or set(item) != {
            "obligation_id", "type", "definition", "evaluation_mode", "criticality", "parameters",
        }:
            raise ValueError("invalid obligation fields")
        oid = _bounded_text(item["obligation_id"], "obligation_id", 96)
        if oid in obligation_ids:
            raise ValueError("duplicate obligation id")
        obligation_ids.add(oid)
        if item["type"] not in OBLIGATION_TYPES:
            raise ValueError("unknown obligation type")
        _bounded_text(item["definition"], "obligation definition")
        if item["evaluation_mode"] not in ("SEMANTIC", "DETERMINISTIC"):
            raise ValueError("invalid obligation evaluation mode")
        if not isinstance(item["parameters"], dict):
            raise ValueError("obligation parameters must be an object")
        if item["type"] in DETERMINISTIC_OBLIGATIONS and item["evaluation_mode"] != "DETERMINISTIC":
            raise ValueError("numeric obligation requires deterministic evaluation")
        if item["type"] not in DETERMINISTIC_OBLIGATIONS and item["evaluation_mode"] != "SEMANTIC":
            raise ValueError("semantic obligation requires semantic evaluation")
        params = item["parameters"]
        if item["type"] == "DELIVERY_DEADLINE":
            if set(params) != {"deadline_timestamp"}:
                raise ValueError("invalid delivery deadline parameters")
            _integer(params["deadline_timestamp"], "obligation deadline")
        elif item["type"] == "MAX_UNIT_PRICE":
            if set(params) != {"order_line_id", "maximum_unit_price_minor"}:
                raise ValueError("invalid maximum unit price parameters")
            _bounded_text(params["order_line_id"], "obligation order line id", 96)
            _integer(params["maximum_unit_price_minor"], "obligation maximum unit price")
        elif item["type"] == "MAX_FREIGHT_CHARGE":
            if set(params) != {"maximum_amount_minor"}:
                raise ValueError("invalid maximum freight parameters")
            _integer(params["maximum_amount_minor"], "maximum freight amount")
        elif item["type"] == "NO_EXTRA_SURCHARGE":
            if set(params) != {"permitted_charge_classes"}:
                raise ValueError("invalid surcharge parameters")
            classes = params["permitted_charge_classes"]
            if not isinstance(classes, list) or len(classes) > 12:
                raise ValueError("invalid permitted charge classes")
            for charge_class in classes:
                _bounded_text(charge_class, "permitted charge class", 64)
        elif params:
            raise ValueError("semantic obligations do not accept deterministic parameters")
        if item["criticality"] not in ("CRITICAL", "STANDARD"):
            raise ValueError("invalid obligation criticality")
    for item in obligations:
        if item["type"] == "MAX_UNIT_PRICE":
            line = next((line for line in lines if line["line_id"] == item["parameters"]["order_line_id"]), None)
            if line is None or item["parameters"]["maximum_unit_price_minor"] > line["max_unit_price_minor"]:
                raise ValueError("maximum unit price obligation must tighten an existing line ceiling")
    return order


def validate_record(raw, kind):
    record = _parse_object(raw, kind)
    expected_record_fields = {"record_id", "order_id", "predecessor_id", "source_reference", "lines", "evidence"}
    if kind == "invoice":
        expected_record_fields.add("invoice_number")
    if set(record) != expected_record_fields:
        raise ValueError("invalid " + kind + " fields")
    _bounded_text(record["record_id"], kind + " record_id", 96)
    _bounded_text(record["order_id"], kind + " order_id", 96)
    if record["predecessor_id"] is not None:
        _bounded_text(record["predecessor_id"], kind + " predecessor_id", 96)
    _bounded_text(record["source_reference"], kind + " source_reference", 160)
    if kind == "invoice":
        _bounded_text(record["invoice_number"], "invoice_number", 96)
    lines = record["lines"]
    if not isinstance(lines, list) or not 1 <= len(lines) <= MAX_LINES:
        raise ValueError(kind + " line count out of bounds")
    ids = set()
    for line in lines:
        fields = {"line_id", "description", "unit", "quantity", "evidence_ref"}
        if kind == "invoice":
            fields |= {"unit_price_minor", "charge_class"}
        if not isinstance(line, dict) or set(line) != fields:
            raise ValueError("invalid " + kind + " line fields")
        lid = _bounded_text(line["line_id"], kind + " line_id", 96)
        if lid in ids:
            raise ValueError("duplicate " + kind + " line id")
        ids.add(lid)
        _bounded_text(line["description"], kind + " description")
        _bounded_text(line["unit"], kind + " unit", 64)
        _positive(line["quantity"], kind + " quantity")
        _bounded_text(line["evidence_ref"], "evidence_ref", 160)
        if kind == "invoice":
            _integer(line["unit_price_minor"], "invoice unit price")
            _bounded_text(line["charge_class"], "charge_class", 64)
    evidence = record["evidence"]
    if not isinstance(evidence, dict) or set(evidence) != {"retrieval_kind", "source", "content"}:
        raise ValueError("invalid " + kind + " evidence")
    if evidence["retrieval_kind"] not in ("STRUCTURED_FIXTURE", "WEB_RENDERED"):
        raise ValueError("unsupported evidence retrieval kind")
    _bounded_text(evidence["source"], "evidence source", 512)
    _bounded_text(evidence["content"], "evidence content", MAX_EVIDENCE_BYTES)
    return record


def validate_proposal(proposal, order, delivery, invoice):
    if not isinstance(proposal, dict) or set(proposal) != {"edges", "obligations", "evidence_sufficient"}:
        raise ValueError("proposal schema invalid")
    if type(proposal["evidence_sufficient"]) is not bool:
        raise ValueError("evidence sufficiency must be bool")
    if not isinstance(proposal["edges"], list) or len(proposal["edges"]) > MAX_LINES * MAX_LINES:
        raise ValueError("edge list invalid")
    order_ids = {x["line_id"] for x in order["lines"]}
    delivery_ids = {x["line_id"] for x in delivery["lines"]}
    invoice_ids = {x["line_id"] for x in invoice["lines"]}
    seen = set()
    seen_delivery = set()
    seen_invoice = set()
    for edge in proposal["edges"]:
        fields = {"order_line_id", "delivery_line_id", "invoice_line_id", "relation", "substitution", "duplicate_class"}
        if not isinstance(edge, dict) or set(edge) != fields:
            raise ValueError("edge schema invalid")
        if edge["order_line_id"] not in order_ids or edge["delivery_line_id"] not in delivery_ids or edge["invoice_line_id"] not in invoice_ids:
            raise ValueError("unknown line id")
        if edge["relation"] not in RELATIONS or edge["substitution"] not in SUBSTITUTIONS:
            raise ValueError("unknown semantic enum")
        if (edge["relation"] == "UNAUTHORIZED_SUBSTITUTION"
                and edge["substitution"] != "UNAUTHORIZED_SUBSTITUTE"):
            raise ValueError("unauthorized relation and substitution finding conflict")
        if (edge["relation"] == "INFERIOR_SUBSTITUTION"
                and edge["substitution"] != "INFERIOR_SUBSTITUTE"):
            raise ValueError("inferior relation and substitution finding conflict")
        if edge["duplicate_class"] not in ("DISTINCT_CHARGE", "POSSIBLE_DUPLICATE_OF_PRIOR_LINE", "SAME_UNDERLYING_CHARGE", "AMBIGUOUS"):
            raise ValueError("unknown duplicate enum")
        key = (edge["order_line_id"], edge["delivery_line_id"], edge["invoice_line_id"])
        if key in seen:
            raise ValueError("duplicate semantic edge")
        if edge["delivery_line_id"] in seen_delivery or edge["invoice_line_id"] in seen_invoice:
            raise ValueError("ambiguous source-line allocation")
        seen.add(key)
        seen_delivery.add(edge["delivery_line_id"])
        seen_invoice.add(edge["invoice_line_id"])
    if not isinstance(proposal["obligations"], dict):
        raise ValueError("obligation findings invalid")
    expected = {x["obligation_id"] for x in order["obligations"] if x["evaluation_mode"] == "SEMANTIC"}
    if set(proposal["obligations"]) != expected:
        raise ValueError("missing or invented obligation findings")
    if any(v not in ("PASS", "FAIL", "AMBIGUOUS", "INSUFFICIENT_EVIDENCE") for v in proposal["obligations"].values()):
        raise ValueError("unknown obligation result")
    if not proposal["evidence_sufficient"]:
        if proposal["edges"]:
            raise ValueError("insufficient evidence proposal cannot assert semantic edges")
        if any(value != "INSUFFICIENT_EVIDENCE" for value in proposal["obligations"].values()):
            raise ValueError("insufficient evidence proposal must fail semantic obligations closed")
        return proposal
    # Every supplied record line must be accounted for, including explicit
    # unrelated/ambiguous findings; omission cannot silently erase a conflict.
    if order_ids and not proposal["edges"]:
        raise ValueError("proposal omitted all order-line findings")
    if delivery_ids - {e["delivery_line_id"] for e in proposal["edges"]}:
        raise ValueError("proposal omitted delivery-line findings")
    if invoice_ids - {e["invoice_line_id"] for e in proposal["edges"]}:
        raise ValueError("proposal omitted invoice-line findings")
    if order_ids - {e["order_line_id"] for e in proposal["edges"]}:
        raise ValueError("proposal omitted order-line findings")
    return proposal
