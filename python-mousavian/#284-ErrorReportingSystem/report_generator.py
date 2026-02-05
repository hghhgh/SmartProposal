from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_str(x: Any) -> str:
    return "" if x is None else str(x)


def _redact_pii(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b(\+?\d[\d\-\s]{7,}\d)\b", "[REDACTED_PHONE]", text)
    return text


@dataclass
class ReferenceErrorItem:
    ref_type: str
    ref_value: str
    error_code: str
    message: str
    field: Optional[str] = None
    source: Optional[str] = None
    occurred_at: Optional[str] = None

    def normalized(self, redact: bool = True) -> Dict[str, Any]:
        d = asdict(self)
        if not d.get("occurred_at"):
            d["occurred_at"] = _utc_now_iso()
        if redact:
            d["ref_value"] = _redact_pii(_safe_str(d["ref_value"]))
            d["message"] = _redact_pii(_safe_str(d["message"]))
        return d


def _summarize(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_code: Dict[str, int] = {}
    by_type: Dict[str, int] = {}

    for it in items:
        by_code[it["error_code"]] = by_code.get(it["error_code"], 0) + 1
        by_type[it["ref_type"]] = by_type.get(it["ref_type"], 0) + 1

    return {
        "total_errors": len(items),
        "by_error_code": dict(sorted(by_code.items(), key=lambda x: (-x[1], x[0]))),
        "by_ref_type": dict(sorted(by_type.items(), key=lambda x: (-x[1], x[0]))),
    }


def generate_reference_error_report(
    errors: Iterable[ReferenceErrorItem],
    *,
    out_dir: str = "reports",
    report_name: Optional[str] = None,
    redact_pii: bool = True,
) -> Dict[str, str]:

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = report_name or f"reference_errors_{stamp}"

    normalized_items = [e.normalized(redact=redact_pii) for e in errors]
    summary = _summarize(normalized_items)

    # JSON
    json_doc = {
        "schema": "reference_error_report",
        "version": "1.0",
        "generated_at": _utc_now_iso(),
        "summary": summary,
        "items": normalized_items,
    }
    json_file = out_path / f"{base}.json"
    json_file.write_text(json.dumps(json_doc, indent=2), encoding="utf-8")

    # CSV
    csv_file = out_path / f"{base}.csv"
    fieldnames = ["occurred_at", "ref_type", "ref_value", "field", "source", "error_code", "message"]
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in normalized_items:
            writer.writerow({k: it.get(k, "") for k in fieldnames})

    # TXT
    txt_file = out_path / f"{base}.txt"
    lines: List[str] = []
    lines.append("Reference Error Report")
    lines.append(f"Generated at: {json_doc['generated_at']}")
    lines.append("")
    lines.append(f"Total errors: {summary['total_errors']}")
    lines.append("")

    if summary["by_error_code"]:
        lines.append("Errors by code:")
        for k, v in summary["by_error_code"].items():
            lines.append(f"  - {k}: {v}")
        lines.append("")

    if summary["by_ref_type"]:
        lines.append("Errors by reference type:")
        for k, v in summary["by_ref_type"].items():
            lines.append(f"  - {k}: {v}")
        lines.append("")

    lines.append("Details:")
    for i, it in enumerate(normalized_items, start=1):
        lines.append(f"{i}. [{it['error_code']}] {it['ref_type']} = {it['ref_value']}")
        if it.get("field"):
            lines.append(f"   Field: {it['field']}")
        if it.get("source"):
            lines.append(f"   Source: {it['source']}")
        lines.append(f"   Message: {it['message']}")
        lines.append(f"   Time: {it['occurred_at']}")
        lines.append("")

    txt_file.write_text("\n".join(lines), encoding="utf-8")

    return {
        "json": str(json_file),
        "csv": str(csv_file),
        "txt": str(txt_file),
    }
