from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

from odf.opendocument import OpenDocumentText

from odf import dc
from extract_odt_metadata import extract_odt_metadata, save_metadata_json


def create_odt_with_metadata(path: str) -> str:
    doc = OpenDocumentText()

    # Real metadata in meta.xml
    doc.meta.addElement(dc.Creator(text="odfpy-test"))
    doc.meta.addElement(dc.Title(text="Sample Title"))
    doc.meta.addElement(dc.Subject(text="Sample Subject"))
    doc.meta.addElement(
        dc.Date(text=datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"))
    )

    doc.save(path)
    return path


def run():
    odt_path = "metadata_sample.odt"
    json_path = "metadata_sample.json"

    create_odt_with_metadata(odt_path)
    assert Path(odt_path).exists(), "ODT file was not created"

    meta = extract_odt_metadata(odt_path)
    assert meta["creator"] == "odfpy-test"
    assert meta["title"] == "Sample Title"
    assert meta["subject"] == "Sample Subject"
    assert meta["creation_date"] == "2024-01-02T03:04:05Z"

    save_metadata_json(odt_path, json_path)
    assert Path(json_path).exists(), "JSON output was not created"

    loaded = json.loads(Path(json_path).read_text(encoding="utf-8"))
    assert loaded == meta, "JSON content does not match extracted metadata"

    print("TEST PASSED")
    print(f"ODT:  {odt_path}")
    print(f"JSON: {json_path}")
    print(loaded)


if __name__ == "__main__":
    run()
