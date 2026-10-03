import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

from config.prompt_loader import load_system_prompt, list_versions, get_active_version
from evaluation.runner import generate_answer
from evaluation.check import run_checks
from evaluation.judge import judge_answer

HERE = Path(__file__).parent


def make_memories(texts: list[str]) -> list[dict]:
    # Make these look EXACTLY like the entries in your real memories.json
    return [{"fact": t} for t in texts]


def mean(values):
    values = [v for v in values if v is not None]
    return statistics.mean(values) if values else None


def evaluate_version(version: str, cases: list[dict]) -> dict:
    system_prompt = load_system_prompt(version)
    rows = []

    for case in cases:
        out = generate_answer(
            system_prompt, make_memories(case["memories"]), case["question"]
        )
        rows.append({
            "id": case["id"],
            "category": case["category"],
            "answer": out["text"],
            "tokens": out["tokens"],
            "latency": out["latency"],
            **run_checks(out["text"], case),
            **judge_answer(case, out["text"]),
        })

    summary = {
        "recall": mean(r["recalled"] for r in rows),
        "leak_rate": mean(r["leaked"] for r in rows),
        "faithfulness": mean(r["faithfulness"] for r in rows),
        "helpfulness": mean(r["helpfulness"] for r in rows),
        "avg_tokens": mean(r["tokens"] for r in rows),
        "avg_latency": mean(r["latency"] for r in rows),
    }
    return {"summary": summary, "rows": rows}


# ---- YOUR DECISION RULE: decide this BEFORE looking at results ----
def beats(candidate: dict, baseline: dict) -> bool:
    g = lambda d, k: d.get(k) or 0
    no_worse_faithfulness = g(candidate, "faithfulness") >= g(baseline, "faithfulness") - 0.02
    no_more_leaks = g(candidate, "leak_rate") <= g(baseline, "leak_rate") + 0.02
    improves = (
        g(candidate, "recall") > g(baseline, "recall")
        or g(candidate, "helpfulness") > g(baseline, "helpfulness") + 0.2
    )
    return no_worse_faithfulness and no_more_leaks and improves


def fmt(x, digits=2):
    return "  n/a" if x is None else f"{x:.{digits}f}"


def main():
    cases = json.loads((HERE / "test_cases.json").read_text(encoding="utf-8"))
    versions = sys.argv[1:] or list_versions()

    results = {}
    for v in versions:
        print(f"Evaluating {v}...")
        results[v] = evaluate_version(v, cases)

    print(f"\n{'version':<8}{'recall':>8}{'leaks':>8}{'faith':>8}{'help':>8}{'tokens':>9}{'secs':>7}")
    for v, r in results.items():
        s = r["summary"]
        print(
            f"{v:<8}{fmt(s['recall']):>8}{fmt(s['leak_rate']):>8}{fmt(s['faithfulness']):>8}"
            f"{fmt(s['helpfulness']):>8}{fmt(s['avg_tokens'], 0):>9}{fmt(s['avg_latency'], 1):>7}"
        )

    baseline = get_active_version()
    if baseline in results:
        print(f"\nBaseline (currently active): {baseline}")
        for v, r in results.items():
            if v != baseline:
                verdict = "BEATS" if beats(r["summary"], results[baseline]["summary"]) else "does NOT beat"
                print(f"  {v} {verdict} {baseline}")

    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"eval_{datetime.now():%Y%m%d_%H%M%S}.json"
    out_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nFull details saved to {out_file}")


if __name__ == "__main__":
    main()