"""Run the extraction eval suite.

Run from the backend folder:  python ../evals/run_evals.py [--min-accuracy 0.85]

Uses the LLM extractor if keys are set, otherwise the rule-based extractor.
Scores each field separately and exits with code 1 if overall accuracy is below the minimum.
TODO (Pair 2): add area and time_window scoring, grow to 100 utterances, save results as EvalRun.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.agent.nodes.extract import rule_based_extract  # noqa: E402
from app.agent.schemas import ServiceRequest  # noqa: E402
from app.llm.router import make_structured_extractor  # noqa: E402

DATASET = Path(__file__).resolve().parent / "dataset.jsonl"
FIELDS = ["service", "urgency", "city"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-accuracy", type=float, default=0.0)
    args = parser.parse_args()

    extractor = make_structured_extractor()
    mode = "llm" if extractor else "rule-based"
    extract = extractor or rule_based_extract

    cases = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line]
    correct: dict[str, int] = defaultdict(int)
    by_language: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    failures: list[str] = []

    for case in cases:
        result: ServiceRequest = extract(case["text"])
        for field in FIELDS:
            ok = getattr(result, field) == case["expected"][field]
            correct[field] += ok
            by_language[case["language"]][0] += ok
            by_language[case["language"]][1] += 1
            if not ok:
                failures.append(
                    f"{case['id']}: {field} expected={case['expected'][field]!r} "
                    f"got={getattr(result, field)!r}"
                )

    total = len(cases) * len(FIELDS)
    overall = sum(correct.values()) / total
    print(f"Mode: {mode} | cases: {len(cases)}")
    for field in FIELDS:
        print(f"  {field:<10} {correct[field] / len(cases):.0%}")
    for lang, (ok, n) in sorted(by_language.items()):
        print(f"  lang {lang:<6} {ok / n:.0%}")
    print(f"Overall: {overall:.0%}")
    if failures:
        print("\nFailures:")
        print("\n".join(f"  {f}" for f in failures))

    if overall < args.min_accuracy:
        print(f"\nFAILED: {overall:.0%} < required {args.min_accuracy:.0%}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
