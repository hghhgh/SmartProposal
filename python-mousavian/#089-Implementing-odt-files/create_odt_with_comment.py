from __future__ import annotations

from datetime import datetime, timezone

from odf.opendocument import OpenDocumentText
from odf import text, office, dc


def add_comment_to_paragraph(paragraph: text.P, comment_text: str, author: str = "System") -> None:
    """
    Insert an ODF annotation (comment) inside a paragraph.
    LibreOffice should render this as a comment.
    """
    ann = office.Annotation()

    ann.addElement(dc.Creator(text=author))
    ann.addElement(dc.Date(text=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")))

    # Comment body
    ann_body = text.P(text=comment_text)
    ann.addElement(ann_body)

    # Add the annotation as an inline element in the paragraph
    paragraph.addElement(ann)


def build_sample_odt(output_path: str = "comment_demo.odt") -> str:
    doc = OpenDocumentText()

    p = text.P()

    # Split text so the annotation is anchored between spans (more reliable in editors)
    p.addElement(text.Span(text="This is a demo paragraph. "))
    add_comment_to_paragraph(
        p,
        comment_text="This is a sample comment created by odfpy.",
        author="odfpy",
    )
    p.addElement(text.Span(text="The comment should be visible in LibreOffice."))

    doc.text.addElement(p)
    doc.save(output_path)

    return output_path


if __name__ == "__main__":
    path = build_sample_odt("comment_demo.odt")
    print(f"Created: {path}")
    print("Open it in LibreOffice and ensure the comment is visible.")
