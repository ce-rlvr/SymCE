"""Inference backends for the eval harness.

Backends share the interface in ``base.py``:

    generate_batch(prompts, n_samples, temperature, max_new_tokens, seed, stop) -> list[list[str]]

so the orchestrator (``training.eval.run_suite``) is backend-agnostic.

Available backends:
- ``vllm_backend.VLLMBackend``: primary local-model path; one engine per
  (model_id, dtype, max_model_len) - load once, reuse across benchmarks.
- ``unsloth_backend.UnslothBackend``: HF/Unsloth fallback for machines without
  vLLM or for the calibration-witness path.
- ``openai_backend.OpenAIBackend``: OpenAI proper and DeepSeek (OpenAI-compatible).
- ``anthropic_backend.AnthropicBackend``: Claude.
- ``gemini_backend.GeminiBackend``: Google ``google.genai``.

``build_backend(spec)`` is the factory the orchestrator calls.
"""

from training.eval.backends.base import Backend, BackendSpec, GenerationRequest

__all__ = ["Backend", "BackendSpec", "GenerationRequest", "build_backend"]


def build_backend(spec: "BackendSpec") -> "Backend":
    """Factory. Lazy-imports the chosen backend to avoid optional deps."""
    kind = spec.kind.lower()
    if kind == "vllm":
        from training.eval.backends.vllm_backend import VLLMBackend
        return VLLMBackend(spec)
    if kind == "unsloth":
        from training.eval.backends.unsloth_backend import UnslothBackend
        return UnslothBackend(spec)
    if kind in ("openai", "deepseek"):
        from training.eval.backends.openai_backend import OpenAIBackend
        return OpenAIBackend(spec)
    if kind == "anthropic":
        from training.eval.backends.anthropic_backend import AnthropicBackend
        return AnthropicBackend(spec)
    if kind == "gemini":
        from training.eval.backends.gemini_backend import GeminiBackend
        return GeminiBackend(spec)
    raise ValueError(f"Unknown backend kind: {spec.kind!r}")
