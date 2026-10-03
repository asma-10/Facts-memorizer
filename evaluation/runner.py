import re
import time

from langchain_groq import ChatGroq

from config.llm import llm as app_llm      # the SAME model your app uses
from nodes.chat import build_messages      # the SAME message-building your app uses

THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)

# Groq free tier for the chat model: ~1000 OUTPUT tokens per minute
OUTPUT_TOKENS_PER_MINUTE = 1000
MAX_OUTPUT_TOKENS = 900  # leave a little headroom for the judge's own text

# The judge is a DIFFERENT model, with temperature 0 so its verdicts are stable
judge_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=3000,
    max_retries=2,
)


def _invoke(model, messages, throttle=False):
    for attempt in range(5):
        try:
            start = time.perf_counter()
            response = model.invoke(messages)
            latency = time.perf_counter() - start
            usage = response.usage_metadata or {}

            result = {
                "text": THINK_RE.sub("", response.content or "").strip(),
                "tokens": usage.get("total_tokens"),
                "latency": latency,
            }

            if throttle:
                # Pause long enough to stay under the per-minute output budget:
                # 300 output tokens -> wait ~18 seconds before the next call.
                out_tokens = usage.get("output_tokens") or 900
                time.sleep(out_tokens / OUTPUT_TOKENS_PER_MINUTE * 60)

            return result

        except Exception as e:
            if "Request too large" in str(e):
                # Retrying can never fix this one: the request itself is over the limit
                raise RuntimeError(
                    "Request exceeds the model's token limit. Lower max_tokens "
                    "in config/llm.py or upgrade your Groq tier."
                ) from e
            wait = 20 * (attempt + 1)  # rate limits reset per minute, so wait longer
            print(f"LLM call failed ({e}); retrying in {wait}s")
            time.sleep(wait)

    raise RuntimeError("LLM call failed after 5 attempts")


def generate_answer(system_prompt, memories, question):
    return _invoke(app_llm, build_messages(system_prompt, memories, question), throttle=True)


def call_judge(messages):
    return _invoke(judge_llm, messages)