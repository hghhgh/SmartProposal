from __future__ import annotations

from dataclasses import dataclass
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


@dataclass(frozen=True)
class LemmaResult:
    token: str
    lemma: str


class TransformerLemmatizer:
    def __init__(self, model_name: str, device: str | None = None) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    @torch.inference_mode()
    def lemmatize_tokens(self, tokens: List[str], max_new_tokens: int = 16) -> List[LemmaResult]:
        results: List[LemmaResult] = []
        for t in tokens:
            inputs = self.tokenizer(t, return_tensors="pt").to(self.device)
            out_ids = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
            lemma = self.tokenizer.decode(out_ids[0], skip_special_tokens=True).strip()
            results.append(LemmaResult(token=t, lemma=lemma))
        return results
