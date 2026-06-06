import json
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "snap-stanford/humanlm-opinion"
PROMPT_MESSAGES = [
    {"role": "user", "content": "Who are you? Please answer briefly."},
]


def main() -> None:
    print(json.dumps({"stage": "load_start", "model": MODEL_NAME}), flush=True)

    load_t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.bfloat16,
        device_map="cpu",
        low_cpu_mem_usage=True,
    )
    model.eval()
    load_s = time.time() - load_t0

    print(
        json.dumps(
            {
                "stage": "load_done",
                "seconds": round(load_s, 2),
                "dtype": str(next(model.parameters()).dtype),
            }
        ),
        flush=True,
    )

    inputs = tokenizer.apply_chat_template(
        PROMPT_MESSAGES,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )
    input_len = inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        gen_t0 = time.time()
        outputs = model.generate(
            **inputs,
            max_new_tokens=32,
            do_sample=False,
            use_cache=True,
        )
        gen_s = time.time() - gen_t0

    new_tokens = outputs.shape[-1] - input_len
    text = tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)

    print(
        json.dumps(
            {
                "stage": "generation_done",
                "input_tokens": int(input_len),
                "new_tokens": int(new_tokens),
                "seconds": round(gen_s, 2),
                "tokens_per_second": round(new_tokens / gen_s, 3) if gen_s > 0 else None,
                "preview": text[:300],
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
