# app/core/dependency_scan.py
import subprocess
import json

def check_vulnerabilities():
    result = subprocess.run(
        ["pip-audit", "--format", "json"],
        capture_output=True,
        text=True
    )

    # اگر pip-audit اجرا نشد
    if result.returncode not in (0, 1):
        raise RuntimeError(f"Dependency scan execution failed: {result.stderr}")

    # returncode == 1 یعنی vulnerability پیدا شده
    if result.stdout:
        data = json.loads(result.stdout)
        return data.get("vulnerabilities", [])

    return []
