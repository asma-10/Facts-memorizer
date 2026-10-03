import json
import re

from evaluation.runner import call_judge

JUDGE_SYSTEM = "You are a strict evaluator of a personalised chatbot. Return ONLY valid JSON."

JUDGE_TEMPLATE = """Stored memories about the user:
{memories}

User question:
{question}

Chatbot answer to evaluate:
{answer}

Tasks:
1. List every statement the answer makes ABOUT THE USER (their life, preferences,
   history, situation). Ignore general knowledge and generic advice.
   Mark "supported": true only if the memories state it or directly imply it.
   Anything else is false (invented).
2. Rate helpfulness from 1 to 5:
   5 = directly answers the question, and uses relevant memories naturally when they exist
   4 = good answer, small flaws
   3 = answers, but generic or awkward
   2 = weak, misses the point, or mentions irrelevant personal details
   1 = unhelpful, wrong, or invents facts about the user

Return JSON in exactly this format:
{{"user_claims": [{{"claim": "...", "supported": true}}], "helpfulness": 4, "reason": "one short sentence"}}"""


def judge_answer(case: dict, answer: str) -> dict:
    memories = "\n".join(f"- {m}" for m in case["memories"]) or "(none)"
    prompt = JUDGE_TEMPLATE.format(
        memories=memories, question=case["question"], answer=answer
    )

    out = call_judge(
        [
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": prompt},
        ]
    )

    try:
        # Grab the first {...} block, in case the judge adds extra text around the JSON
        data = json.loads(re.search(r"\{.*\}", out["text"], re.DOTALL).group(0))
        claims = data["user_claims"]
        faithfulness = (
            1.0 if not claims else sum(1 for c in claims if c["supported"]) / len(claims)
        )
        return {
            "faithfulness": faithfulness,
            "helpfulness": data["helpfulness"],
            "unsupported": [c["claim"] for c in claims if not c["supported"]],
            "judge_reason": data["reason"],
        }
    except Exception:
        # A failed judgment becomes None, so it is ignored in the averages
        # instead of crashing the whole run.
        return {
            "faithfulness": None,
            "helpfulness": None,
            "unsupported": [],
            "judge_reason": "JUDGE FAILED",
        }