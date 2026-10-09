"""Compare local contract bytes to an explicitly fetched chain source file."""
import argparse
import hashlib
import sys
import urllib.error
import urllib.request
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-url", required=True, help="verified chain source endpoint URL")
    parser.add_argument("--contract", default="contracts/semantic_reconciliation.py")
    args = parser.parse_args()
    local = Path(args.contract).read_bytes()
    request = urllib.request.Request(args.source_url, headers={"User-Agent": "semantic-reconciliation-source-parity/1"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            remote = response.read(2_000_001)
    except (OSError, urllib.error.URLError) as exc:
        print(f"UNVERIFIED: source endpoint unavailable: {type(exc).__name__}", file=sys.stderr)
        return 2
    if len(remote) > 2_000_000:
        print("FAIL: source exceeds parity size limit", file=sys.stderr)
        return 1
    local_hash, remote_hash = sha256(local), sha256(remote)
    print(f"local_sha256={local_hash}")
    print(f"remote_sha256={remote_hash}")
    print(f"match={local_hash == remote_hash}")
    return 0 if local == remote else 1


if __name__ == "__main__":
    raise SystemExit(main())
