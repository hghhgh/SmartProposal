from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from odf.opendocument import load
from odf import office, text, dc


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _get_paragraph_text(p: text.P) -> str:
    # Best-effort extraction without extra deps.
    parts: List[str] = []
    for node in p.childNodes:
        if getattr(node, "data", None) is not None:
            parts.append(str(node.data))
        else:
            # Some children can be spans, annotations, etc.
            # Try to read their firstChild.data if present.
            fc = getattr(node, "firstChild", None)
            if fc is not None and getattr(fc, "data", None) is not None:
                parts.append(str(fc.data))
    return "".join(parts).strip()


def analyze_document(doc) -> Dict[str, int]:
    paragraphs = doc.text.getElementsByType(text.P)
    para_count = len(paragraphs)

    word_count = 0
    for p in paragraphs:
        s = _get_paragraph_text(p)
        if s:
            word_count += len(s.split())

    return {"paragraph_count": para_count, "word_count": word_count}


def add_comment_to_first_paragraph(doc, comment_text: str, author: str = "pipeline") -> None:
    paragraphs = doc.text.getElementsByType(text.P)

    # If the document has no paragraphs, create one.
    if not paragraphs:
        p = text.P()
        p.addElement(text.Span(text=" "))
        doc.text.addElement(p)
        paragraphs = [p]

    p0 = paragraphs[0]

    ann = office.Annotation
