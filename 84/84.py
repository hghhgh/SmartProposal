```python
from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional, Dict, Any
import json


class Level(str, Enum):
    REQUIRED = "اجباری"
    RECOMMENDED = "توصیه"
    OPTIONAL = "خوب است"


@dataclass(frozen=True)
class Position:
    section: str
    paragraph: int
    offset: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section": self.section,
            "paragraph": self.paragraph,
            "offset": self.offset,
        }


@dataclass(frozen=True)
class Suggestion:
    level: Level
    text: str
    position: Position
    replacement_example: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "text": self.text,
            "position": self.position.to_dict(),
            "replacement_example": self.replacement_example,
        }

    def validate(self) -> None:
        if not isinstance(self.level, Level):
            raise ValueError("invalid level")
        if not self.text or not isinstance(self.text, str):
            raise ValueError("invalid text")
        if not isinstance(self.position, Position):
            raise ValueError("invalid position")
        if self.position.paragraph < 0:
            raise ValueError("paragraph must be >= 0")


class SuggestionStore:
    def __init__(self) -> None:
        self._data: Dict[str, Suggestion] = {}

    def add(self, key: str, suggestion: Suggestion) -> None:
        suggestion.validate()
        if key in self._data:
            raise KeyError("duplicate key")
        self._data[key] = suggestion

    def get(self, key: str) -> Suggestion:
        return self._data[key]

    def to_json(self) -> str:
        payload = {k: v.to_dict() for k, v in self._data.items()}
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @staticmethod
    def from_json(raw: str) -> "SuggestionStore":
        obj = json.loads(raw)
        store = SuggestionStore()
        for k, v in obj.items():
            s = Suggestion(
                level=Level(v["level"]),
                text=v["text"],
                position=Position(**v["position"]),
                replacement_example=v.get("replacement_example"),
            )
            store.add(k, s)
        return store


# -------- tests --------
if __name__ == "__main__":
    store = SuggestionStore()

    s1 = Suggestion(
        level=Level.REQUIRED,
        text="استفاده از فعل مجهول کاهش یابد.",
        position=Position(section="مقدمه", paragraph=2, offset=15),
        replacement_example="جمله به صورت معلوم بازنویسی شود."
    )

    s2 = Suggestion(
        level=Level.RECOMMENDED,
        text="عنوان بخش شفاف‌تر شود.",
        position=Position(section="نتیجه‌گیری", paragraph=0),
        replacement_example="نتایج و جمع‌بندی نهایی"
    )

    store.add("SUG-001", s1)
    store.add("SUG-002", s2)

    js = store.to_json()
    restored = SuggestionStore.from_json(js)

    assert restored.get("SUG-001").to_dict() == s1.to_dict()
    assert restored.get("SUG-002").to_dict() == s2.to_dict()
    assert "اجباری" in js and "توصیه" in js
```
