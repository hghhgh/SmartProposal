from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional

from hazm import Normalizer, Stemmer, Lemmatizer


@dataclass(frozen=True)
class TokenResult:
    token: str
    normalized: str
    stem: str
    lemma: str


class PersianRooter:
    """
    Persian stemming + lemmatization pipeline using Hazm.
    """
    def __init__(self) -> None:
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.lemmatizer = Lemmatizer()

    def process_tokens(self, tokens: List[str]) -> List[TokenResult]:
        out: List[TokenResult] = []
        for t in tokens:
            n = self.normalizer.normalize(t)
            stem = self.stemmer.stem(n) or ""
            lemma = self.lemmatizer.lemmatize(n) or ""
            out.append(TokenResult(token=t, normalized=n, stem=stem, lemma=lemma))
        return out

    def process_text(self, text: str) -> List[TokenResult]:
        # Minimal tokenization to avoid additional deps; user can plug Hazm word_tokenize if needed.
        tokens = [x for x in text.split() if x.strip()]
        return self.process_tokens(tokens)
