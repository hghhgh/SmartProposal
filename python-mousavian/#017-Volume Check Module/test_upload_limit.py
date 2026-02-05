from __future__ import annotations

import httpx

BASE_URL = "http://localhost:8000"
MAX_BYTES = 20 * 1024 * 1024  # keep in sync with server


def run():
    # 1) Allowed file (MAX_BYTES - 1)
    small = b"a" * (MAX_BYTES - 1)
    r1 = httpx.post(
        f"{BASE_URL}/upload",
        files={"file": ("small.bin", small, "application/octet-stream")},
        timeout=60,
    )
    assert r1.status_code == 200, f"Expected 200, got {r1.status_code}: {r1.text}"
    assert r1.json().get("ok") is True
    assert r1.json().get("size") == (MAX_BYTES - 1)

    # 2) Too large file (MAX_BYTES + 1) -> 413
    big = b"b" * (MAX_BYTES + 1)
    r2 = httpx.post(
        f"{BASE_URL}/upload",
        files={"file": ("big.bin", big, "application/octet-stream")},
        timeout=60,
    )
    assert r2.status_code == 413, f"Expected 413, got {r2.status_code}: {r2.text}"
    assert r2.json().get("ok") is False

    print("TEST PASSED")
    print("small upload: OK")
    print("big upload: REJECTED (413)")


if __name__ == "__main__":
    run()
