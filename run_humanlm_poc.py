import argparse
import json
import time
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer


DEFAULT_MODEL = "snap-stanford/humanlm-opinion"
DEFAULT_COMPARE_MODELS = [
    "snap-stanford/humanlm-opinion",
    "Qwen/Qwen3-8B",
]
DEFAULT_SCENARIOS = Path("scenarios/poc_cognitive_dissonance.json")
DEFAULT_OUTPUT_DIR = Path("outputs")


def slugify_model_name(model_name: str) -> str:
    return (
        model_name.lower()
        .replace("/", "__")
        .replace("-", "_")
        .replace(".", "_")
    )


def build_staa_prompt(scenario: dict) -> str:
    knowledge_lines = "\n".join(
        f"- {item}" for item in scenario.get("knowledge", [])
    )
    return f"""You are simulating one human user.

Below is the person's internal state.

Knowledge:
{knowledge_lines}

Opinion:
- {scenario["opinion"]}

Task:
Answer as this person would answer. The answer may be imperfect or conflicted, but it should still feel believable and human.

Question:
{scenario["question"]}

Output format:
Return valid JSON with exactly these keys:
- "behavior_choice": a short description of what the person does or chooses
- "reason": a short first-person justification

Important instructions:
- Write only one JSON object.
- Start directly with `{{`.
- Do not include analysis.
- Do not include chain-of-thought.
- Do not explain the task.
- Do not write any text before the JSON object.
- Do not write any text after the JSON object.
- Keep the answer short and complete.
"""


def build_revb_prompt(scenario: dict) -> str:
    knowledge_lines = "\n".join(
        f"- {item}" for item in scenario.get("knowledge", [])
    )
    return f"""You are simulating one human user.

Below is the person's internal state.

Knowledge:
{knowledge_lines}

Opinion:
- {scenario["opinion"]}

Question:
{scenario["question"]}

Continue the person's answer naturally.

Important instructions:
- Write only the continuation of the answer.
- Do not explain the task.
- Do not analyze.
- Do not say "the user", "the person", or "this person".
- Do not use `<think>` or hidden reasoning.
- Stay in character and continue the answer directly.

Answer:
I would"""


def build_inputs(tokenizer: AutoTokenizer, prompt: str) -> dict[str, torch.Tensor]:
    messages = [{"role": "user", "content": prompt}]
    return tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )


def decode_token(tokenizer: AutoTokenizer, token_id: int) -> str:
    return tokenizer.decode([token_id], skip_special_tokens=False)


def run_staa(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    scenario: dict,
    max_new_tokens: int,
) -> dict:
    prompt = build_staa_prompt(scenario)
    inputs = build_inputs(tokenizer, prompt)
    input_len = inputs["input_ids"].shape[-1]

    gen_t0 = time.time()
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            use_cache=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )
    gen_s = time.time() - gen_t0
    text = tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True).strip()

    return {
        "prompt": prompt,
        "raw_output": text,
        "input_tokens": int(input_len),
        "new_tokens": int(outputs.shape[-1] - input_len),
        "seconds": round(gen_s, 2),
        "tokens_per_second": round((outputs.shape[-1] - input_len) / gen_s, 3) if gen_s > 0 else None,
    }


def run_revb(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    scenario: dict,
    max_new_tokens: int,
    top_k: int,
) -> dict:
    prompt = build_revb_prompt(scenario)
    inputs = build_inputs(tokenizer, prompt)
    input_len = inputs["input_ids"].shape[-1]

    gen_t0 = time.time()
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            use_cache=True,
            output_scores=True,
            return_dict_in_generate=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )
    gen_s = time.time() - gen_t0

    generated_ids = outputs.sequences[0][input_len:]
    continuation_text = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    token_steps = []

    for step_idx, (token_id, step_scores) in enumerate(zip(generated_ids.tolist(), outputs.scores), start=1):
        probs = F.softmax(step_scores[0], dim=-1)
        chosen_prob = probs[token_id].item()
        top_probs, top_ids = torch.topk(probs, k=min(top_k, probs.shape[-1]))

        token_steps.append(
            {
                "step": step_idx,
                "token_id": int(token_id),
                "token_text": decode_token(tokenizer, int(token_id)),
                "token_probability": round(chosen_prob, 8),
                "top_candidates": [
                    {
                        "token_id": int(candidate_id),
                        "token_text": decode_token(tokenizer, int(candidate_id)),
                        "probability": round(candidate_prob.item(), 8),
                    }
                    for candidate_prob, candidate_id in zip(top_probs, top_ids)
                ],
            }
        )

    return {
        "prompt": prompt,
        "continuation_text": continuation_text,
        "input_tokens": int(input_len),
        "new_tokens": int(generated_ids.shape[-1]),
        "seconds": round(gen_s, 2),
        "tokens_per_second": round(generated_ids.shape[-1] / gen_s, 3) if gen_s > 0 else None,
        "token_steps": token_steps,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--models",
        nargs="+",
        help="Run multiple models in one script execution. Example: --models snap-stanford/humanlm-opinion Qwen/Qwen3-8B",
    )
    parser.add_argument(
        "--compare-default-models",
        action="store_true",
        help="Run the default comparison pair: HumanLM and Qwen3-8B.",
    )
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-new-tokens", type=int, default=96)
    parser.add_argument("--revb-max-new-tokens", type=int, default=8)
    parser.add_argument("--revb-top-k", type=int, default=5)
    return parser.parse_args()


def resolve_models(args: argparse.Namespace) -> list[str]:
    if args.models:
        return args.models
    if args.compare_default_models:
        return DEFAULT_COMPARE_MODELS
    return [args.model]


def run_for_model(
    model_name: str,
    scenarios: list[dict],
    args: argparse.Namespace,
) -> dict:
    print(json.dumps({"stage": "load_start", "model": model_name}), flush=True)
    load_t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="cpu",
        low_cpu_mem_usage=True,
    )
    model.eval()
    print(
        json.dumps(
            {
                "stage": "load_done",
                "model": model_name,
                "seconds": round(time.time() - load_t0, 2),
                "dtype": str(next(model.parameters()).dtype),
                "scenario_count": len(scenarios),
            }
        ),
        flush=True,
    )

    results = []

    for scenario in scenarios:
        staa = run_staa(model, tokenizer, scenario, args.max_new_tokens)
        revb = run_revb(
            model,
            tokenizer,
            scenario,
            args.revb_max_new_tokens,
            args.revb_top_k,
        )

        record = {
            "scenario_id": scenario["id"],
            "title": scenario["title"],
            "domain": scenario["domain"],
            "stated_answer": staa,
            "revealed_belief": revb,
        }
        results.append(record)
        print(
            json.dumps(
                {
                    "stage": "scenario_done",
                    "model": model_name,
                    "scenario_id": scenario["id"],
                    "staa_seconds": staa["seconds"],
                    "revb_seconds": revb["seconds"],
                    "revb_continuation": revb["continuation_text"],
                }
            ),
            flush=True,
        )

    return {
        "model": model_name,
        "model_slug": slugify_model_name(model_name),
        "results": results,
    }


def main() -> None:
    args = parse_args()
    scenarios = json.loads(args.scenarios.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    models = resolve_models(args)

    run_id = time.strftime("%Y%m%d_%H%M%S")
    if len(models) == 1:
        output_stem = f"poc_{slugify_model_name(models[0])}_{run_id}"
    else:
        output_stem = f"poc_multi_model_{run_id}"
    output_path = args.output_dir / f"{output_stem}.json"

    model_runs = []
    for model_name in models:
        model_runs.append(run_for_model(model_name, scenarios, args))

    summary = {
        "run_id": run_id,
        "scenario_file": str(args.scenarios),
        "models_run": models,
        "staa_max_new_tokens": args.max_new_tokens,
        "revb_max_new_tokens": args.revb_max_new_tokens,
        "revb_top_k": args.revb_top_k,
        "model_runs": model_runs,
    }
    output_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"stage": "run_done", "output_path": str(output_path)}), flush=True)


if __name__ == "__main__":
    main()
