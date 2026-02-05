from __future__ import annotations

import zipfile
from pathlib import Path

from create_odt_with_comment import build_sample_odt


def run():
    out = build_sample_odt("comment_demo_test.odt")
    assert Path(out).exists(), "ODT was not created"

    with zipfile.ZipFile(out, "r") as z:
        content_xml = z.read("content.xml").decode("utf-8", errors="replace")

    assert "office:annotation" in content_xml, "Annotation element not found in content.xml"
    assert "This is a sample comment created by odfpy." in content_xml, "Comment text not found in content.xml"

    print("TEST PASSED")
    print(f"Generated: {out}")
    print("Manual verification step: open in LibreOffice and confirm the comment is visible.")


if __name__ == "__main__":
    run()
