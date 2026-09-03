"""vLLM-backed local inference.

Loads a single ``vllm.LLM`` engine for the lifetime of the backend (re-used
across benchmarks within one suite invocation). When the input is a runs/sft
or runs/rlvr directory we auto-prefer the ``merged/`` subdir - this avoids
the Unsloth↔vLLM LoRA-format mismatch.

LoRA-on-base-model serving is also supported via ``--enable-lora`` at engine
init plus a per-request ``LoRARequest``; we only use it when the user
explicitly passes ``lora_adapter`` AND no merged path is found.
"""

from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

from training.eval.backends.base import (
    Backend,
    BackendSpec,
    GenerationRequest,
    GenerationResult,
)
from training.eval.cache import get_cache, make_cache_key

logger = logging.getLogger(__name__)


def _resolve_local_model_path(model_id: str) -> tuple[str, Optional[str]]:
    """If model_id is a runs/sft or runs/rlvr dir, prefer the merged/ subdir.

    Returns (model_path_for_vllm, lora_adapter_path_or_none).
    """
    p = Path(model_id)
    if p.is_dir():
        merged = p / "merged"
        lora = p / "lora"
        if merged.exists() and any(merged.iterdir()):
            logger.info("vLLM: using merged checkpoint at %s", merged)
            return str(merged), None
        if lora.exists() and any(lora.iterdir()):
            # Fall through: we'll use enable_lora and a LoRARequest.
            # The base model is recorded in adapter_config.json (auto-loaded
            # by vLLM via the lora subdir).
            logger.info("vLLM: merged/ missing; will load lora at %s", lora)
            return str(p), str(lora)
    # HF hub id or absolute path -> pass through.
    return model_id, None


class VLLMBackend(Backend):
    def __init__(self, spec: BackendSpec):
        super().__init__(spec)
        self._llm = None
        self._tokenizer = None
        self._lora_request = None
        self._resolved_model: Optional[str] = None

    def _lazy_load(self) -> None:
        if self._loaded:
            return
        try:
            from vllm import LLM, SamplingParams  # noqa: F401  (SamplingParams imported in generate_batch)
        except ImportError as e:
            raise RuntimeError(
                "vLLM is not installed. `pip install vllm` (CUDA wheel) or switch "
                "the backend to `unsloth` in your eval config."
            ) from e

        model_path = self.spec.model_id
        explicit_lora = self.spec.lora_adapter
        if explicit_lora:
            resolved_model = model_path
            resolved_lora = explicit_lora
        else:
            resolved_model, resolved_lora = _resolve_local_model_path(model_path)

        self._resolved_model = resolved_model

        engine_kwargs = dict(
            model=resolved_model,
            dtype=self.spec.dtype,
            max_model_len=self.spec.max_model_len,
            gpu_memory_utilization=self.spec.gpu_memory_utilization,
            tensor_parallel_size=self.spec.tensor_parallel_size,
            trust_remote_code=self.spec.trust_remote_code,
        )
        if resolved_lora is not None:
            engine_kwargs["enable_lora"] = True
            engine_kwargs["max_lora_rank"] = int(self.spec.extra.get("max_lora_rank", 32))

        logger.info("vLLM engine init: %s", {k: v for k, v in engine_kwargs.items() if k != "model"})
        logger.info("  model = %s", resolved_model)
        t0 = time.time()
        self._llm = LLM(**engine_kwargs)
        logger.info("vLLM engine loaded in %.1fs", time.time() - t0)

        self._tokenizer = self._llm.get_tokenizer()

        if resolved_lora is not None:
            from vllm.lora.request import LoRARequest
            self._lora_request = LoRARequest(
                lora_name=Path(resolved_lora).name,
                lora_int_id=1,
                lora_path=resolved_lora,
            )

        self._loaded = True

    # Prompt rendering
    def render_prompt(self, messages: list[dict]) -> str:
        self._lazy_load()
        # apply_chat_template returns the rendered string that we'll cache + feed.
        try:
            return self._tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True,
            )
        except Exception as e:
            logger.warning(
                "tokenizer.apply_chat_template failed (%s); falling back to role-join", e
            )
            return super().render_prompt(messages)

    # Main entry point
    def generate_batch(
        self, requests: list[GenerationRequest]
    ) -> list[list[GenerationResult]]:
        if not requests:
            return []
        self._lazy_load()
        from vllm import SamplingParams

        cache = get_cache()
        model_key = self._resolved_model or self.spec.model_id
        if self._lora_request is not None:
            # Disambiguate cache entries when serving LoRA adapters.
            lora_name = getattr(self._lora_request, "lora_path", None) or "lora"
            model_key = f"{model_key}|lora={lora_name}"
        results: list[list[Optional[GenerationResult]]] = [
            [None] * r.n_samples for r in requests
        ]

        # First pass: render prompts + cache lookups.
        rendered: list[str] = [self.render_prompt(r.messages) for r in requests]
        # Sanitize sampling per request (greedy + N>1 -> collapse to N=1).
        sanitized = []
        for r in requests:
            temp, n, _ = Backend.sanitize_sampling(r.temperature, r.n_samples)
            sanitized.append((temp, n))

        # Resize per-request result lists if sanitize collapsed n_samples.
        for i, (_, n) in enumerate(sanitized):
            if n != requests[i].n_samples:
                results[i] = [None] * n

        misses: list[tuple[int, int, str, float, int, int, float]] = []
        # (req_idx, sample_idx, prompt, temperature, max_new_tokens, top_p_seed, ...)
        # We use seed = base_seed + sample_idx for reproducibility.
        for i, (req, prompt) in enumerate(zip(requests, rendered)):
            temp, n_eff = sanitized[i]
            for s_idx in range(n_eff):
                key = make_cache_key(
                    model_key,
                    prompt + (req.cache_key_extra or ""),
                    s_idx,
                    temp,
                    req.top_p,
                    req.max_new_tokens,
                    req.stop,
                )
                hit = cache.get(key)
                if hit is not None:
                    results[i][s_idx] = GenerationResult(
                        text=hit, sample_idx=s_idx, cached=True
                    )
                else:
                    misses.append((i, s_idx, prompt, temp, req.max_new_tokens,
                                   req.seed + s_idx, req.top_p))

        if not misses:
            return [[r for r in row if r is not None] for row in results]

        # vLLM batches better when prompts with identical sampling params go
        # through a single ``llm.generate`` call. Group misses by (temp, max_new, top_p).
        groups: dict[tuple[float, int, float], list[tuple[int, int, str, int]]] = {}
        for (i, s_idx, prompt, temp, max_new, seed, top_p) in misses:
            groups.setdefault((temp, max_new, top_p), []).append((i, s_idx, prompt, seed))

        n_total_misses = len(misses)
        t0 = time.time()
        for (temp, max_new, top_p), items in groups.items():
            sp = SamplingParams(
                n=1,                       # we already replicated via sample_idx
                temperature=float(temp),
                top_p=float(top_p),
                max_tokens=int(max_new),
                stop=requests[items[0][0]].stop,
            )
            prompts = [it[2] for it in items]
            seeds = [it[3] for it in items]
            kwargs = {"sampling_params": sp}
            if self._lora_request is not None:
                kwargs["lora_request"] = self._lora_request
            # vLLM supports per-request seeds via SamplingParams(seed=...);
            # we vary it by re-issuing in batches grouped by seed when needed.
            # For simplicity: one SamplingParams per unique seed (cheap).
            by_seed: dict[int, list[int]] = {}
            for j, s in enumerate(seeds):
                by_seed.setdefault(s, []).append(j)
            for s, js in by_seed.items():
                sp_s = SamplingParams(
                    n=1, temperature=float(temp), top_p=float(top_p),
                    max_tokens=int(max_new), seed=int(s),
                    stop=requests[items[js[0]][0]].stop,
                )
                sub_prompts = [prompts[j] for j in js]
                outs = self._llm.generate(sub_prompts, sp_s, **{
                    k: v for k, v in kwargs.items() if k != "sampling_params"
                })
                for j_local, out in zip(js, outs):
                    i_req, s_idx, prompt, _seed = items[j_local]
                    text = out.outputs[0].text
                    stop_reason = out.outputs[0].finish_reason
                    results[i_req][s_idx] = GenerationResult(
                        text=text, sample_idx=s_idx, cached=False,
                        stop_reason=stop_reason,
                    )
                    # Write through to cache
                    key = make_cache_key(
                        model_key,
                        prompt + (requests[i_req].cache_key_extra or ""),
                        s_idx,
                        temp,
                        requests[i_req].top_p,
                        max_new,
                        requests[i_req].stop,
                    )
                    cache.put(
                        key,
                        model_id=model_key,
                        prompt=prompt + (requests[i_req].cache_key_extra or ""),
                        sample_idx=s_idx,
                        temperature=temp,
                        max_new_tokens=max_new,
                        completion=text,
                        stop_reason=stop_reason,
                    )

        elapsed = time.time() - t0
        logger.info(
            "vLLM generated %d completions across %d prompts in %.1fs (%.2f tok/s est.)",
            n_total_misses, len(set(i for i, _, _, _, _, _, _ in misses)),
            elapsed,
            n_total_misses * 256 / max(elapsed, 1e-6),
        )

        return [[r for r in row if r is not None] for row in results]

    def close(self) -> None:
        if self._llm is not None:
            # vLLM doesn't expose a clean shutdown API; rely on GC + CUDA cleanup.
            try:
                del self._llm
            except Exception:
                pass
            self._llm = None
        self._loaded = False
