def contains_any(text: str, words: list[str]) -> bool:
    text = text.lower()
    return any(w.lower() in text for w in words)


def run_checks(answer: str, case: dict) -> dict:
    # None means "this check doesn't apply to this test case"
    recalled = None
    if case.get("must_mention_any"):
        recalled = 1.0 if contains_any(answer, case["must_mention_any"]) else 0.0

    leaked = None
    if case.get("must_not_mention"):
        leaked = 1.0 if contains_any(answer, case["must_not_mention"]) else 0.0

    return {"recalled": recalled, "leaked": leaked}