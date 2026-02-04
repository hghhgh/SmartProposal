import re
from typing import List, Dict


URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
HTML_PATTERN = re.compile(r'<[^>]+>')
MENTION_PATTERN = re.compile(r'[@#]\w+')
NON_ALPHA_PATTERN = re.compile(r'^[^a-zA-Z\u0600-\u06FF]+$')


def normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def char_diversity_ratio(text: str) -> float:
    unique_chars = set(text)
    return len(unique_chars) / max(len(text), 1)


def token_count(text: str) -> int:
    return len(text.split())


def is_noise(text: str) -> bool:
    if not text or not text.strip():
        return True

    text = normalize(text)

    if URL_PATTERN.search(text):
        return True
    if HTML_PATTERN.search(text):
        return True
    if MENTION_PATTERN.search(text):
        return True
    if NON_ALPHA_PATTERN.match(text):
        return True
    if token_count(text) < 3:
        return True
    if char_diversity_ratio(text) < 0.25:
        return True

    return False


def clean_texts(texts: List[str]) -> Dict[str, float | List[str]]:
    original_count = len(texts)
    cleaned_texts = [normalize(t) for t in texts if not is_noise(t)]

    noise_ratio = 1 - (len(cleaned_texts) / original_count if original_count else 0)

    return {
        "cleaned_texts": cleaned_texts,
        "noise_reduction_percent": round(noise_ratio * 100, 2)
    }


def test_noise_reduction():
    texts = [
        "",
        "https://spam.com",
        "<p>hello</p>",
        "خخخخخخخخ",
        "ok",
        "Machine learning models are evaluated using cross validation",
        "در این مقاله یک روش جدید برای تحلیل داده‌ها ارائه می‌شود",
        "Statistical significance is measured using p-values",
        "test test test test"
    ]

    result = clean_texts(texts)

    assert result["noise_reduction_percent"] >= 90, "Noise reduction below expected threshold"
    assert len(result["cleaned_texts"]) >= 2, "Valid scientific texts removed"

    return result


if __name__ == "__main__":
    print(test_noise_reduction())
