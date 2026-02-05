from dataclasses import dataclass
from typing import Dict, List
from enum import Enum
import json


class RuleLevel(str, Enum):
    MANDATORY = "mandatory"
    RECOMMENDATION = "recommendation"
    WARNING = "warning"


@dataclass(frozen=True)
class SectionRule:
    required: bool
    min_length: int
    order: int


class StructuralKnowledgeBase:
    def __init__(self, rules: Dict[str, SectionRule]):
        self.rules = rules

    @classmethod
    def from_json(cls, path: str) -> "StructuralKnowledgeBase":
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        rules = {}
        for name, data in raw.items():
            rules[name] = SectionRule(
                required=bool(data["required"]),
                min_length=int(data["min_length"]),
                order=int(data["order"]),
            )

        return cls(rules)


class StructuralAnalyzer:
    def __init__(self, knowledge_base: StructuralKnowledgeBase):
        self.kb = knowledge_base

    def analyze(self, document_structure: Dict[str, str]) -> List[Dict]:
        findings: List[Dict] = []

        self._check_required_sections(document_structure, findings)
        self._check_minimum_content(document_structure, findings)
        self._check_order(document_structure, findings)

        return findings

    def _check_required_sections(
        self, document_structure: Dict[str, str], findings: List[Dict]
    ):
        for section, rule in self.kb.rules.items():
            if rule.required and section not in document_structure:
                findings.append({
                    "level": RuleLevel.MANDATORY.value,
                    "section": section,
                    "message": "بخش الزامی وجود ندارد"
                })

    def _check_minimum_content(
        self, document_structure: Dict[str, str], findings: List[Dict]
    ):
        for section, content in document_structure.items():
            rule = self.kb.rules.get(section)
            if rule and len(content.strip()) < rule.min_length:
                findings.append({
                    "level": RuleLevel.RECOMMENDATION.value,
                    "section": section,
                    "message": "حداقل محتوای مورد انتظار رعایت نشده"
                })

    def _check_order(
        self, document_structure: Dict[str, str], findings: List[Dict]
    ):
        actual_order = [
            section for section in document_structure
            if section in self.kb.rules
        ]

        expected_order = [
            name for name, _ in sorted(
                self.kb.rules.items(),
                key=lambda item: item[1].order
            )
            if name in actual_order
        ]

        if actual_order != expected_order:
            findings.append({
                "level": RuleLevel.WARNING.value,
                "section": actual_order,
                "message": "ترتیب بخش‌ها مطابق دانش ساختاری نیست"
            })


# ===== Example Usage =====
# kb = StructuralKnowledgeBase.from_json("structure_rules.json")
# analyzer = StructuralAnalyzer(kb)
# result = analyzer.analyze(parsed_document_structure)
