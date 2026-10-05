"""AI Knowledge Assistant -- Version 5: Production AI System (Chapter 11).

A minimal golden-dataset evaluation harness using LLM-as-a-judge, plus a
simple cost/latency log -- the two lightest-weight, highest-leverage
practices from Chapter 11, applied to the Version 2 RAG assistant.

Requires OPENAI_API_KEY (the judge call, and rag_answer's generation step,
both call a real model).

Run:
    OPENAI_API_KEY=sk-... python evaluate.py
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "v2_rag_application"))
from rag_assistant import rag_answer  # noqa: E402

GOLDEN_DATASET = [
    {"question": "How long do I have to return a product?",
     "expected_fact": "30 days with a receipt"},
    {"question": "How fast are High urgency tickets answered?",
     "expected_fact": "within 1 hour"},
]

COST_LOG: list[dict] = []


def judge_answer(question: str, answer: str, expected_fact: str) -> bool:
    """LLM-as-a-judge: does the answer correctly convey the expected fact?"""
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # illustrative model name -- see Chapter 1's note
        messages=[{"role": "user", "content":
            f"Question: {question}\nAnswer: {answer}\n"
            f"Does the answer correctly convey this fact: '{expected_fact}'? "
            "Reply with only YES or NO."}],
        temperature=0,
    )
    return resp.choices[0].message.content.strip().upper().startswith("YES")


def timed_rag_answer(question: str) -> str:
    start = time.perf_counter()
    answer = rag_answer(question)
    elapsed = time.perf_counter() - start
    COST_LOG.append({"question": question, "latency_seconds": round(elapsed, 2)})
    return answer


def run_evaluation() -> None:
    passed = 0
    for case in GOLDEN_DATASET:
        answer = timed_rag_answer(case["question"])
        correct = judge_answer(case["question"], answer, case["expected_fact"])
        print(f"[{'PASS' if correct else 'FAIL'}] {case['question']}")
        passed += correct
    print(f"\n{passed}/{len(GOLDEN_DATASET)} passed")
    print("\nCost/latency log:")
    for entry in COST_LOG:
        print(f"  {entry['latency_seconds']:.2f}s  {entry['question']}")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit(
            "Set OPENAI_API_KEY before running this script -- "
            "Version 5's evaluation harness calls a real LLM judge."
        )
    run_evaluation()
