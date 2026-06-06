import argparse
import json
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


DEFAULT_MODEL = "snap-stanford/humanlm-opinion"
DEFAULT_SCENARIOS = Path("scenarios/poc_cognitive_dissonance.json")
DEFAULT_OUTPUT_DIR = Path("outputs")


def build_prompt(scenario: dict) -> str:
    knowledge_lines = "\n".join(
        f"- {item}" for item in scenario.get("knowledge", [])
    )
    return f"""You are simulating one human user.

Below is the user's internal state.

Knowledge:
{knowledge_lines}

Opinion:
- {scenario["opinion"]}

Task:
Answer as this person would answer. The answer may be imperfect or conflicted, but it should still feel like a believable human answer.

Question:
{scenario["question"]}

Output format:
Return valid JSON with exactly these keys:
- "behavior": a short description of what the person does or chooses
- "reason": a short first-person justification
- "dissonance_type": choose one of ["consistent", "human_like_dissonance", "artifact_like"]
- "confidence": number from 0 to 1
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-new-tokens", type=int, default=160)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenarios = json.loads(args.scenarios.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(json.dumps({"stage": "load_start", "model": args.model}), flush=True)
    load_t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16,
        device_map="cpu",
        low_cpu_mem_usage=True,
    )
    model.eval()
    print(
        json.dumps(
            {
                "stage": "load_done",
                "seconds": round(time.time() - load_t0, 2),
                "dtype": str(next(model.parameters()).dtype),
                "scenario_count": len(scenarios),
            }
        ),
        flush=True,
    )

    run_id = time.strftime("%Y%m%d_%H%M%S")
    output_path = args.output_dir / f"humanlm_poc_{run_id}.json"
    results = []

    for scenario in scenarios:
        messages = [{"role": "user", "content": build_prompt(scenario)}]
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )

        input_len = inputs["input_ids"].shape[-1]
        gen_t0 = time.time()
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
                use_cache=True,
            )
        gen_s = time.time() - gen_t0
        text = tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True).strip()

        record = {
            "scenario_id": scenario["id"],
            "title": scenario["title"],
            "domain": scenario["domain"],
            "prompt": messages[0]["content"],
            "raw_output": text,
            "input_tokens": int(input_len),
            "new_tokens": int(outputs.shape[-1] - input_len),
            "seconds": round(gen_s, 2),
            "tokens_per_second": round((outputs.shape[-1] - input_len) / gen_s, 3) if gen_s > 0 else None,
        }
        results.append(record)
        print(json.dumps({"stage": "scenario_done", **{k: record[k] for k in ["scenario_id", "seconds", "tokens_per_second"]}}), flush=True)

    summary = {
        "model": args.model,
        "run_id": run_id,
        "scenario_file": str(args.scenarios),
        "results": results,
    }
    output_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"stage": "run_done", "output_path": str(output_path)}), flush=True)


if __name__ == "__main__":
    main()
