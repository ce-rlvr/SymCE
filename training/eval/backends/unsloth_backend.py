"""Unsloth / HuggingFace fallback backend.

Preserves the original generation path from ``training/eval/eval_runner.py``
so machines without vLLM can still run evals. Also used by the
canonical-witness calibration mode (it doesn't actually call generate but
needs a backend object).
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

import torch

from training.eval.backends.base import (
    Backend,
    BackendSpec,
    GenerationRequest,
    GenerationResult,
)
from training.eval.cache import get_cache, make_cache_key

logger = logging.getLogger(__name__)


class UnslothBackend(Backend):
    def __init__(self, spec: BackendSpec):
        super().__init__(spec)
        self._model = None
        self._tokenizer = None

    def _lazy_load(self) -> None:
        if self._loaded:
            return
        from unsloth import FastLanguageModel
        from training.common.chat_template import apply_chat_template

        dtype_map = {
            "bfloat16": torch.bfloat16,
            "float16": torch.float16,
            "float32": torch.float32,
        }
        dtype = dtype_map[self.spec.dtype]

        load_path = self.spec.lora_adapter or self.spec.model_id
        logger.info("Unsloth loading: %s", load_path)
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=load_path,
            max_seq_length=self.spec.max_model_len,
            dtype=dtype,
            load_in_4bit=False,
        )
        tokenizer = apply_chat_template(
            tokenizer,
            model_name=self.spec.model_id,
            chat_template=self.spec.chat_template,
            checkpoint_path=Path(self.spec.lora_adapter) if self.spec.lora_adapter else None,
        )
        FastLanguageModel.for_inference(model)
        self._model = model
        self._tokenizer = tokenizer
        self._loaded = True

    def render_prompt(self, messages: list[dict]) -> str:
        self._lazy_load()
        return self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
        )

    def generate_batch(
        self, requests: list[GenerationRequest]
    ) -> list[list[GenerationResult]]:
        if not requests:
            return []
        self._lazy_load()
        cache = get_cache()
        results: list[list[Optional[GenerationResult]]] = []
        model_key = self.spec.model_id
        if self.spec.lora_adapter:
            model_key = f"{model_key}|lora={self.spec.lora_adapter}"

        for req_idx, req in enumerate(requests):
            temp, n_eff, _ = Backend.sanitize_sampling(req.temperature, req.n_samples)
            prompt = self.render_prompt(req.messages)
            row: list[Optional[GenerationResult]] = [None] * n_eff

            # Cache lookups
            uncached_idxs: list[int] = []
            for s_idx in range(n_eff):
                key = make_cache_key(
                    model_key,
                    prompt + (req.cache_key_extra or ""),
                    s_idx, temp, req.top_p,
                    req.max_new_tokens,
                    req.stop,
                )
                hit = cache.get(key)
                if hit is not None:
                    row[s_idx] = GenerationResult(text=hit, sample_idx=s_idx, cached=True)
                else:
                    uncached_idxs.append(s_idx)

            if uncached_idxs:
                inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
                n_uncached = len(uncached_idxs)
                batched_inputs = {k: v.expand(n_uncached, -1) for k, v in inputs.items()}
                do_sample = temp > 0.0
                gen_kwargs = dict(
                    max_new_tokens=req.max_new_tokens,
                    pad_token_id=self._tokenizer.pad_token_id or self._tokenizer.eos_token_id,
                    do_sample=do_sample,
                    temperature=temp if do_sample else 1.0,
                    use_cache=True,
                )
                if do_sample:
                    torch.manual_seed(req.seed + uncached_idxs[0])

                with torch.no_grad():
                    out_ids = self._model.generate(**batched_inputs, **gen_kwargs)
                prompt_len = inputs["input_ids"].shape[1]
                for k, s_idx in enumerate(uncached_idxs):
                    new_tokens = out_ids[k][prompt_len:]
                    text = self._tokenizer.decode(new_tokens, skip_special_tokens=True)
                    row[s_idx] = GenerationResult(text=text, sample_idx=s_idx, cached=False)
                    # Cache write
                    key = make_cache_key(
                        model_key,
                        prompt + (req.cache_key_extra or ""),
                        s_idx, temp, req.top_p,
                        req.max_new_tokens,
                        req.stop,
                    )
                    cache.put(
                        key,
                        model_id=model_key,
                        prompt=prompt + (req.cache_key_extra or ""),
                        sample_idx=s_idx,
                        temperature=temp,
                        max_new_tokens=req.max_new_tokens,
                        completion=text,
                    )

            results.append([r for r in row if r is not None])

        return results

    def close(self) -> None:
        # Release CUDA memory if possible.
        if self._model is not None:
            try:
                del self._model
            except Exception:
                pass
            self._model = None
            self._tokenizer = None
            torch.cuda.empty_cache()
        self._loaded = False
