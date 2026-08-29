"""Anthropic / Claude backend.

System messages go into the dedicated ``system`` field (Anthropic doesn't
accept role='system' in messages). Concurrency + retries mirror the OpenAI
backend so the orchestrator can treat them uniformly.
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


class AnthropicBackend(Backend):
    def __init__(self, spec: BackendSpec):
        super().__init__(spec)
        self._client = None

    def _lazy_load(self) -> None:
        if self._loaded:
            return
        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise RuntimeError(
                "anthropic SDK not installed. `pip install anthropic`."
            ) from e
        api_key_env = self.spec.api_key_env or "ANTHROPIC_API_KEY"
        api_key = os.environ.get(api_key_env)
        if not api_key:
            raise RuntimeError(f"{api_key_env} not set.")
        self._client = Anthropic(api_key=api_key, base_url=self.spec.base_url or None)
        self._loaded = True

    def _split_system(self, messages: list[dict]) -> tuple[str, list[dict]]:
        system_parts = [m["content"] for m in messages if m.get("role") == "system"]
        non_system = [m for m in messages if m.get("role") != "system"]
        return ("\n\n".join(system_parts).strip(), non_system)

    def _one_call(
        self,
        messages: list[dict],
        temperature: float,
        max_new_tokens: int,
        top_p: float,
    ) -> tuple[str, Optional[str]]:
        system_text, body = self._split_system(messages)
        last_err: Optional[Exception] = None
        for attempt in range(self.spec.max_retries):
            try:
                resp = self._client.messages.create(
                    model=self.spec.model_id,
                    system=system_text or None,
                    messages=body,
                    max_tokens=int(max_new_tokens),
                    temperature=float(temperature),
                    top_p=float(top_p),
                    timeout=self.spec.request_timeout_seconds,
                )
                # Concatenate text blocks (Claude can return multiple).
                texts = []
                for blk in resp.content:
                    if getattr(blk, "type", "") == "text":
                        texts.append(blk.text)
                return ("".join(texts), getattr(resp, "stop_reason", None))
            except Exception as e:
                last_err = e
                sleep_s = min(60.0, (2 ** attempt) + random.uniform(0.0, 0.5))
                logger.warning(
                    "Anthropic call failed (attempt %d/%d): %s; sleeping %.1fs",
                    attempt + 1, self.spec.max_retries, e, sleep_s,
                )
                time.sleep(sleep_s)
        raise RuntimeError(f"Anthropic API failed after {self.spec.max_retries} retries: {last_err}")

    def generate_batch(
        self, requests: list[GenerationRequest]
    ) -> list[list[GenerationResult]]:
        if not requests:
            return []
        self._lazy_load()
        cache = get_cache()
        results: list[list[Optional[GenerationResult]]] = [[None] * r.n_samples for r in requests]

        tasks = []
        for i, r in enumerate(requests):
            temp, n_eff, _ = Backend.sanitize_sampling(r.temperature, r.n_samples)
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
                    tasks.append((i, s_idx, r.messages, temp, r.max_new_tokens, r.top_p, prompt_str))

        if not tasks:
            return [[g for g in row if g is not None] for row in results]

        max_workers = max(1, int(self.spec.max_concurrent_requests))
        logger.info("Anthropic: %d misses, max_concurrent=%d", len(tasks), max_workers)
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_to_meta = {
                pool.submit(self._one_call, msgs, temp, max_new, top_p):
                    (i, s_idx, prompt_str, temp, max_new)
                for (i, s_idx, msgs, temp, max_new, top_p, prompt_str) in tasks
            }
            for fut in as_completed(future_to_meta):
                i, s_idx, prompt_str, temp, max_new = future_to_meta[fut]
                text, stop_reason = fut.result()
                results[i][s_idx] = GenerationResult(
                    text=text, sample_idx=s_idx, cached=False, stop_reason=stop_reason
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
                    stop_reason=stop_reason,
                )
        logger.info("Anthropic done in %.1fs", time.time() - t0)
        return [[g for g in row if g is not None] for row in results]
