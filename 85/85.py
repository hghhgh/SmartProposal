from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum
import random


class Severity(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Level(Enum):
    REQUIRED = "اجباری"
    RECOMMENDED = "توصیه"
    OPTIONAL = "خوب است"


class Category(Enum):
    GRAMMAR = "grammar"
    STYLE = "style"
    CONTENT = "content"
    OTHER = "other"  # برای دسته‌بندی ناشناخته


@dataclass(frozen=True)
class AnalysisIssue:
    code: str
    category: Category
    severity: Severity
    message: str
    line: Optional[int] = None
    char: Optional[int] = None


@dataclass(frozen=True)
class Suggestion:
    level: Level
    text: str
    issue_code: str
    line: Optional[int] = None
    char: Optional[int] = None


class SuggestionEngine:
    def __init__(self) -> None:
        # قالب‌ها برای هر دسته و سطح
        self._templates: Dict[Category, Dict[Level, List[str]]] = {
            Category.GRAMMAR: {
                Level.REQUIRED: [
                    "خطای نگارشی جدی در این بخش مشاهده شد (خط {line}). اصلاح فوری لازم است.",
                    "نگارش این جمله اشتباه است و باید اصلاح شود (خط {line})."
                ],
                Level.RECOMMENDED: [
                    "ساختار نگارشی این جمله می‌تواند بهبود یابد (خط {line}).",
                    "بازبینی نگارش این بخش توصیه می‌شود (خط {line})."
                ],
                Level.OPTIONAL: [
                    "می‌توان نگارش این بخش را روان‌تر کرد.",
                    "اصلاح جزئی نگارش می‌تواند متن را واضح‌تر کند."
                ]
            },
            Category.STYLE: {
                Level.REQUIRED: [
                    "سبک نوشتار این بخش با استاندارد متن همخوانی ندارد.",
                    "این بخش نیاز به بازنویسی فوری برای تطابق با سبک متن دارد."
                ],
                Level.RECOMMENDED: [
                    "بهتر است سبک نوشتار یکنواخت‌تر شود.",
                    "اصلاح سبک نوشتار به خوانایی متن کمک می‌کند."
                ],
                Level.OPTIONAL: [
                    "می‌توان سبک نوشتار را برای وضوح بهتر بهبود داد."
                ]
            },
            Category.CONTENT: {
                Level.REQUIRED: [
                    "محتوای این بخش ناقص یا نادقیق است و باید اصلاح شود.",
                    "این بخش اطلاعات مهمی را از دست داده است (خط {line})."
                ],
                Level.RECOMMENDED: [
                    "توضیحات این بخش می‌تواند دقیق‌تر باشد.",
                    "بهتر است محتوای این بخش کامل‌تر شود."
                ],
                Level.OPTIONAL: [
                    "در صورت نیاز، می‌توان محتوای این بخش را تکمیل کرد."
                ]
            },
            Category.OTHER: {
                Level.REQUIRED: [
                    "این بخش دارای خطای مهمی است و نیاز به اصلاح فوری دارد.",
                    "مشکلات این بخش باید سریعاً برطرف شود."
                ],
                Level.RECOMMENDED: [
                    "بهتر است این بخش بازبینی و اصلاح شود.",
                    "بازبینی این بخش می‌تواند کیفیت متن را افزایش دهد."
                ],
                Level.OPTIONAL: [
                    "می‌توان این بخش را برای وضوح و خوانایی بهتر بازبینی کرد."
                ]
            }
        }

    def generate(self, issues: List[AnalysisIssue]) -> List[Suggestion]:
        suggestions: List[Suggestion] = []

        for issue in issues:
            level = self._map_severity(issue.severity)
            category = issue.category if issue.category in self._templates else Category.OTHER
            templates = self._templates[category][level]
            text = self._choose_template(templates, issue)

            suggestions.append(
                Suggestion(
                    level=level,
                    text=text,
                    issue_code=issue.code,
                    line=issue.line,
                    char=issue.char
                )
            )

        return suggestions

    @staticmethod
    def _map_severity(severity: Severity) -> Level:
        mapping = {
            Severity.HIGH: Level.REQUIRED,
            Severity.MEDIUM: Level.RECOMMENDED,
            Severity.LOW: Level.OPTIONAL
        }
        return mapping.get(severity, Level.RECOMMENDED)

    @staticmethod
    def _choose_template(templates: List[str], issue: AnalysisIssue) -> str:
        # انتخاب تصادفی قالب برای تنوع پیام
        template = random.choice(templates)
        return template.format(line=issue.line or "نامشخص")


# مثال تست
if __name__ == "__main__":
    issues = [
        AnalysisIssue(
            code="G001",
            category=Category.GRAMMAR,
            severity=Severity.HIGH,
            message="خطای فعل و فاعل",
            line=12,
            char=5
        ),
        AnalysisIssue(
            code="C010",
            category=Category.CONTENT,
            severity=Severity.LOW,
            message="توضیح ناکافی",
            line=30,
            char=1
        ),
        AnalysisIssue(
            code="X999",
            category=Category.OTHER,
            severity=Severity.MEDIUM,
            message="دسته‌بندی ناشناخته",
            line=45
        )
    ]

    engine = SuggestionEngine()
    result = engine.generate(issues)

    for s in result:
        print(f"{s.level.value} | {s.text} | کد خطا: {s.issue_code} | خط: {s.line}")
