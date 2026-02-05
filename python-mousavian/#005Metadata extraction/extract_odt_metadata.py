from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from odf.opendocument import load
from odf import dc


def _first_text(el) -> Optional[str]:
    if el is None:
        return None
    # odfpy elements store text in firstChild.data for simple nodes
    try:
        if el.firstChild and getattr(el.firstChild, "data", None) is not None:
            return str(el.firstChild.data)
    except Exception:
        pass
    return None


def extract_odt_metadata(odt_path: str) -> Dict[str, Any]:
    """
    Extracts core metadata fields from an ODT using odfpy.
    Returns a dict with keys:
      - creator
      - title
      - subject
      - creation_date
    """
    doc = load(odt_path)
    meta = getattr(doc, "meta", None)

    # Defaults
    result = {
        "creator": None,
        "title": None,
        "subject": None,
        "creation_date": None,
    }

    if meta is None:
        return result

    # dc:* fields in meta.xml
    creator_el = meta.getElementsByType(dc.Creator)
    title_el = meta.getElementsByType(dc.Title)
    subject_el = meta.getElementsByType(dc.Subject)
    date_el = meta.getElementsByType(dc.Date)

    result["creator"] = _first_text(creator_el[0]) if creator_el else None
    result["title"] = _first_text(title_el[0]) if title_el else None
    result["subject"] = _first_text(subject_el[0]) if subject_el else None
    result["creation_date"] = _first_text(date_el[0]) if date_el else None

    return result


def save_metadata_json(odt_path: str, json_path: str) -> str:
    data = extract_odt_metadata(odt_path)
    Path(json_path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return json_path


if __name__ == "__main__":
    # Example usage:
    # python extract_odt_metadata.py input.odt output.json
    import sys

    if len(sys.argv) != 3:
        print("Usage: python extract_odt_metadata.py <input.odt> <output.json>")
        raise SystemExit(2)

    in_odt, out_json = sys.argv[1], sys.argv[2]
    save_metadata_json(in_odt, out_json)
    print(f"Wrote: {out_json}")
