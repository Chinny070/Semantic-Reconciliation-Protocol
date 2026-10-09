"""Zero-dependency local source and fixture preflight."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "contracts"))
import protocol


def main() -> int:
    checks = [
        ("order fixture", ROOT / "fixtures/order/po-cement.json", lambda raw: protocol.validate_order(raw)),
        ("delivery fixture", ROOT / "fixtures/delivery/delivery-cement.json", lambda raw: protocol.validate_record(raw, "delivery")),
        ("invoice fixture", ROOT / "fixtures/invoice/invoice-cement.json", lambda raw: protocol.validate_record(raw, "invoice")),
    ]
    for label, path, validate in checks:
        value = json.loads(path.read_text(encoding="utf-8"))
        validate(json.dumps(value, separators=(",", ":")))
        print(f"PASS {label}: {path.relative_to(ROOT)}")
    print("PASS bounded protocol fixture preflight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
