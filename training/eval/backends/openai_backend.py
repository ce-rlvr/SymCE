"""OpenAI + DeepSeek backend (OpenAI-compatible chat completions API).

Matches the existing pattern in ``tools/inject_witness_schema.py``:

    from openai import OpenAI
    client = OpenAI(api_key=..., base_url=...)   # base_url is None for OpenAI proper

Concurrency: bounded ThreadPoolExecutor. Retries with exponential backoff on
rate-limit + transient errors.
"""

from __future__ import annotations

import logging
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

from training.eval.backends.base import (
    Backend,
    BackendSpec,
    GenerationRequest,
    GenerationResult,
)
from training.eval.cache import get_cache, make_cache_key

logger = logging.getLogger(__name__)


class OpenAIBackend(Backend):
    def __init__(self, spec: BackendSpec):
        super().__init__(spec)
        self._client = None

    def _lazy_load(self) -> None:
        if self._loaded:
            return
        try:
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError(
                "openai SDK not installed. `pip install openai` (already present "
                "as a dependency of the deepseek wiring in tools/inject_witness_schema.py)."
            ) from e

        api_key_env = self.spec.api_key_env or (
            "DEEPSEEK_API_KEY" if self.spec.kind.lower() == "deepseek" else "OPENAI_API_KEY"
        )
        api_key = os.environ.get(api_key_env)
        if not api_key:
            raise RuntimeError(
                f"{api_key_env} not set. Add it to .env or your shell environment."
            )

        kwargs = {"api_key": api_key}
        if self.spec.base_url:
            kwargs["base_url"] = self.spec.base_url
        elif self.spec.kind.lower() == "deepseek":
            kwargs["base_url"] = "https://api.deepseek.com"

        self._client = OpenAI(**kwargs)
        self._loaded = True

    def render_prompt(self, messages: list[dict]) -> str:
        # No tokenizer; just a deterministic string for the cache key.
        return super().render_prompt(messages)

    def _one_call(
        self,
        messages: list[dict],
        temperature: float,
        max_new_tokens: int,
        seed: int,
        top_p: float,
    ) -> tuple[str, Optional[str]]:
        last_err: Optional[Exception] = None
        for attempt in range(self.spec.max_retries):
            try:
                resp = self._client.chat.completions.create(
                    model=self.spec.model_id,
                    messages=messages,
                    temperature=float(temperature),
                    max_tokens=int(max_new_tokens),
                    top_p=float(top_p),
                    seed=int(seed),
                    timeout=self.spec.request_timeout_seconds,
                )
                choice = resp.choices[0]
                return (choice.message.content or "", choice.finish_reason)
            except Exception as e:
                last_err = e
                # Exponential backoff with jitter; cap at 60s
                sleep_s = min(60.0, (2 ** attempt) + random.uniform(0.0, 0.5))
                logger.warning(
                    "%s API call failed (attempt %d/%d): %s; sleeping %.1fs",
                    self.spec.kind, attempt + 1, self.spec.max_retries, e, sleep_s,
                )
                time.sleep(sleep_s)
        raise RuntimeError(
            f"{self.spec.kind} API failed after {self.spec.max_retries} retries: {last_err}"
        )

    def generate_batch(
        self, requests: list[GenerationRequest]
    ) -> list[list[GenerationResult]]:
        if not requests:
            return []
        self._lazy_load()
        cache = get_cache()
        results: list[list[Optional[GenerationResult]]] = [[None] * r.n_samples for r in requests]

        # Sanitize n_samples; collect cache misses.
        tasks: list[tuple[int, int, list[dict], float, int, int, float, str]] = []
        sanitized: list[tuple[float, int]] = []
        for i, r in enumerate(requests):
            temp, n_eff, _ = Backend.sanitize_sampling(r.temperature, r.n_samples)
            sanitized.append((temp, n_eff))
            if n_eff != r.n_samples:
                results[i] = [None] * n_eff
            prompt_str = self.render_prompt(r.messages)
            for s_idx in range(n_eff):
                key = make_cache_key(
                    self.spec.model_id,
                    prompt_str + (r.cache_key_extra or ""),
                    s_idx, temp, r.top_p, r.max_new_tokens, r.stop,
                )
                hit = cache.get(key)
                if hit is not None:
                    results[i][s_idx] = GenerationResult(text=hit, sample_idx=s_idx, cached=True)
                else:
                    tasks.append((i, s_idx, r.messages, temp, r.max_new_tokens,
                                  r.seed + s_idx, r.top_p, prompt_str))

        if not tasks:
            return [[g for g in row if g is not None] for row in results]

        max_workers = max(1, int(self.spec.max_concurrent_requests))
        logger.info(
            "%s API: %d cache misses across %d prompts, max_concurrent=%d",
            self.spec.kind, len(tasks), len(requests), max_workers,
        )
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_to_task = {
                pool.submit(
                    self._one_call, msgs, temp, max_new, seed, top_p
                ): (i, s_idx, prompt_str, temp, max_new)
                for (i, s_idx, msgs, temp, max_new, seed, top_p, prompt_str) in tasks
            }
            for fut in as_completed(future_to_task):
                i, s_idx, prompt_str, temp, max_new = future_to_task[fut]
                text, finish_reason = fut.result()
                results[i][s_idx] = GenerationResult(
                    text=text, sample_idx=s_idx, cached=False, stop_reason=finish_reason
                )
                key = make_cache_key(
                    self.spec.model_id,
                    prompt_str + (requests[i].cache_key_extra or ""),
                    s_idx, temp, requests[i].top_p, max_new, requests[i].stop,
                )
                cache.put(
                    key,
                    model_id=self.spec.model_id,
                    prompt=prompt_str + (requests[i].cache_key_extra or ""),
                    sample_idx=s_idx,
                    temperature=temp,
                    max_new_tokens=max_new,
                    completion=text,
                    stop_reason=finish_reason,
                )
        logger.info("%s API done in %.1fs", self.spec.kind, time.time() - t0)
        return [[g for g in row if g is not None] for row in results]
