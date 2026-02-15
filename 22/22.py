from lxml import etree
from typing import List, Dict, Any


class XMLStructureAnalyzer:
    def __init__(self, xml_path: str):
        self.tree = etree.parse(xml_path)
        self.root = self.tree.getroot()
        self.ns = self._normalize_namespaces()

    def _normalize_namespaces(self) -> Dict[str, str]:
        nsmap = {}
        for k, v in self.root.nsmap.items():
            nsmap[k if k else "ns"] = v
        return nsmap

    def _xpath(self, expr: str):
        return self.root.xpath(expr, namespaces=self.ns)

    def analyze(self) -> Dict[str, Any]:
        return {
            "headings": self._extract_headings(),
            "paragraphs": self._extract_paragraphs(),
            "lists": self._extract_lists(),
            "tables": self._extract_tables(),
            "images": self._extract_images()
        }

    def _extract_headings(self) -> List[Dict]:
        result = []
        for level in range(1, 7):
            for el in self._xpath(f"//ns:h{level}"):
                result.append({
                    "level": level,
                    "text": "".join(el.itertext()).strip(),
                    "position": self._position(el)
                })
        return result

    def _extract_paragraphs(self) -> List[Dict]:
        return [
            {
                "text": "".join(p.itertext()).strip(),
                "position": self._position(p)
            }
            for p in self._xpath("//ns:p")
        ]

    def _extract_lists(self) -> List[Dict]:
        lists = []
        for el in self._xpath("//ns:ul | //ns:ol"):
            lists.append({
                "type": "ordered" if el.tag.endswith("ol") else "unordered",
                "items": [
                    "".join(li.itertext()).strip()
                    for li in el.xpath(".//ns:li", namespaces=self.ns)
                ],
                "position": self._position(el)
            })
        return lists

    def _extract_tables(self) -> List[Dict]:
        tables = []
        for table in self._xpath("//ns:table"):
            rows = []
            for row in table.xpath(".//ns:tr", namespaces=self.ns):
                cells = []
                for cell in row.xpath("./ns:td | ./ns:th", namespaces=self.ns):
                    cells.append({
                        "text": "".join(cell.itertext()).strip(),
                        "colspan": int(cell.get("colspan", 1)),
                        "rowspan": int(cell.get("rowspan", 1))
                    })
                rows.append(cells)
            tables.append({
                "rows": rows,
                "position": self._position(table)
            })
        return tables

    def _extract_images(self) -> List[Dict]:
        return [
            {
                "src": img.get("src"),
                "alt": img.get("alt"),
                "position": self._position(img)
            }
            for img in self._xpath("//ns:img | //ns:image")
        ]

    def _position(self, el) -> int:
        return len(el.xpath("preceding::*"))


def analyze_structure(xml_path: str) -> Dict[str, Any]:
    analyzer = XMLStructureAnalyzer(xml_path)
    return analyzer.analyze()


if __name__ == "__main__":
    result = analyze_structure("sample.xml")
    print(result)
