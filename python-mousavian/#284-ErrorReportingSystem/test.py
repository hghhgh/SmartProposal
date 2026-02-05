from pathlib import Path
import json
import csv

from report_generator import ReferenceErrorItem, generate_reference_error_report


def run():
    errors = [
        ReferenceErrorItem(
            ref_type="document_id",
            ref_value="doc_404",
            error_code="NOT_FOUND",
            message="Document not found.",
            field="documents[0].id",
            source="user_input",
        ),
        ReferenceErrorItem(
            ref_type="url",
            ref_value="https://example.com/private/report.pdf",
            error_code="FORBIDDEN",
            message="Access to the URL is forbidden.",
            field="attachments[2].url",
            source="import",
        ),
        ReferenceErrorItem(
            ref_type="record_id",
            ref_value="123-INVALID",
            error_code="INVALID_FORMAT",
            message="Invalid record identifier format.",
            field="records[5].id",
            source="api",
        ),
    ]

    paths = generate_reference_error_report(
        errors,
        out_dir="reports",
        report_name="sample_reference_error_report",
        redact_pii=True,
    )

    for p in paths.values():
        assert Path(p).exists(), f"File not created: {p}"

    doc = json.loads(Path(paths["json"]).read_text(encoding="utf-8"))
    assert doc["summary"]["total_errors"] == 3

    with open(paths["csv"], newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert len(rows) == 4

    txt = Path(paths["txt"]).read_text(encoding="utf-8")
    assert "Reference Error Report" in txt

    print("TEST PASSED")
    for k, p in paths.items():
        print(f"{k}: {p}")


if __name__ == "__main__":
    run()
