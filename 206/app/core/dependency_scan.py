import subprocess
from app.core.security_events import log_event

def run_dependency_scan():
    try:
        result = subprocess.run(
            ["pip-audit", "--format", "json"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            findings = result.stdout.strip()

            log_event(
                "DEPENDENCY_VULNERABILITY",
                {
                    "tool": "pip-audit",
                    "findings": findings
                }
            )

            return {
                "status": "vulnerable",
                "details": findings
            }

        return {
            "status": "clean",
            "details": []
        }

    except Exception as e:
        log_event(
            "DEPENDENCY_SCAN_ERROR",
            {"error": str(e)}
        )
        raise
