"""Backend ABC + shared types.

A Backend takes rendered chat messages (list-of-dicts with role/content) and
returns ``n_samples`` completions per prompt. It owns:

- Model loading / API client setup (lazy on first call).
- Chat-template application (so the prompt-string the cache sees is the same
  string that gets fed to the model — critical for cache reuse).
- Sampling-vs-greedy semantics:
    * temperature == 0.0  → deterministic; if n_samples > 1 the backend
      MUST log a warning and either bump the temperature OR collapse to a
      single sample with a warning. The Pass@K bug we shipped previously
      came from expanding a greedy prompt to N copies — never again.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class BackendSpec:
    """Config for a backend instance.

    The orchestrator pulls this out of ``configs/eval/<name>.yaml`` per model.
    """
    kind: str                           # vllm | unsloth | openai | deepseek | anthropic | gemini
    model_id: str                       # HF id, local path, or API model name
    display_name: Optional[str] = None  # for run-summary rendering
    # Local-model knobs
    lora_adapter: Optional[str] = None  # only for unsloth / vllm-lora
    dtype: str = "bfloat16"
    max_model_len: int = 4096
    gpu_memory_utilization: float = 0.85
    tensor_parallel_size: int = 1
    trust_remote_code: bool = True
    chat_template: str = "auto"         # passed to training.common.chat_template
    # API knobs
    api_key_env: Optional[str] = None   # env var holding the key
    base_url: Optional[str] = None      # e.g. https://api.deepseek.com
    max_concurrent_requests: int = 8
    request_timeout_seconds: float = 120.0
    max_retries: int = 5
    # Per-backend pass-throughs
    extra: dict = field(default_factory=dict)


@dataclass
class GenerationRequest:
    """One prompt's generation request. Chat-template is applied by the backend."""
    messages: list[dict]                # [{"role": ..., "content": ...}, ...]
    n_samples: int = 1
    temperature: float = 0.0
    max_new_tokens: int = 1024
    top_p: float = 1.0
    seed: int = 42
    stop: Optional[list[str]] = None
    # Cache identity context — the backend writes through to the cache using
    # this. ``cache_key_extra`` is appended to the cache key to disambiguate
    # otherwise-identical requests (e.g., prompt-style label).
    cache_key_extra: str = ""


@dataclass
class GenerationResult:
    """One completion. ``cached`` is True if returned from the cache."""
    text: str
    sample_idx: int
    cached: bool = False
    stop_reason: Optional[str] = None


class Backend(ABC):
    """Abstract backend. Subclasses load lazily on first generate_batch call."""

    def __init__(self, spec: BackendSpec):
        self.spec = spec
        self._loaded = False

    @property
    def model_id(self) -> str:
        return self.spec.model_id

    @property
    def display_name(self) -> str:
        return self.spec.display_name or self.spec.model_id

    def render_prompt(self, messages: list[dict]) -> str:
        """Render messages into the string the model will actually see.

        Local backends override this to apply the tokenizer's chat template.
        API backends typically don't need it (the API handles roles directly)
        but we still need a stable string for cache keys — the default
        implementation produces a deterministic role-tagged join.
        """
        parts = []
        for m in messages:
            parts.append(f"<|{m['role']}|>\n{m['content']}\n")
        return "".join(parts)

    @abstractmethod
    def generate_batch(
        self, requests: list[GenerationRequest]
    ) -> list[list[GenerationResult]]:
        """Generate completions for all requests.

        Returns a list of length ``len(requests)``; each entry is a list of
        ``request.n_samples`` GenerationResults (in sample-idx order).
        Backends are responsible for cache lookups + writes.
        """
        ...

    def close(self) -> None:
        """Release model / connection resources. Default: no-op."""
        return None

    # ── Safety net: enforce sane sampling parameters ─────────────────────────
    @staticmethod
    def sanitize_sampling(temperature: float, n_samples: int) -> tuple[float, int, bool]:
        """Common guard against the pass@k-equals-pass@1 bug.

        Returns (temperature, n_samples, was_corrected). If T==0 and N>1,
        we COLLAPSE to N=1 with a clear warning — preferable to silently
        bumping the temperature, which would change the user-visible
        sampling distribution.
        """
        if temperature <= 0.0 and n_samples > 1:
            logger.warning(
                "Greedy sampling (temperature=0) requested with n_samples=%d; "
                "all samples would be identical. Collapsing to n_samples=1. "
                "Set temperature>0 (e.g. 0.7) for true Pass@K sampling.",
                n_samples,
            )
            return temperature, 1, True
        return temperature, n_samples, False
