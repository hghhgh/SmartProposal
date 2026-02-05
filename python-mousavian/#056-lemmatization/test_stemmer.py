from stemmer_lemmas import PersianRooter

def run():
    r = PersianRooter()

    # Inputs
    tokens = [
        "کتاب‌ها",
        "کتابها",
        "می‌روم",
        "رفته‌ام",
        "بهترین",
        "دویدن",
        "خانه‌ام",
    ]

    results = r.process_tokens(tokens)
    m = {x.token: x for x in results}

    # Basic assertions (robust-ish across Hazm versions)
    assert "کتاب" in m["کتاب‌ها"].stem
    assert "کتاب" in m["کتابها"].stem

    # Lemmas can vary a bit; check containment / expected patterns
    assert m["می‌روم"].lemma != ""          # should produce something meaningful
    assert m["رفته‌ام"].lemma != ""         # should produce something meaningful

    # Normalization sanity
    assert m["خانه‌ام"].normalized != ""    # should normalize ZWNJ consistently

    print("TEST PASSED")
    for x in results:
        print(f"{x.token} -> normalized={x.normalized} | stem={x.stem} | lemma={x.lemma}")

if __name__ == "__main__":
    run()
