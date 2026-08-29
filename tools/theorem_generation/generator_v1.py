import json
import logging
import os
import re
import threading
import time
import uuid
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from tqdm import tqdm

# ============================================================
# CONFIG
# ============================================================

OUTPUT_FILE = "synthetic_theorems.json"

TARGET_THEOREMS = 2500
MAX_LOOPS = 350

THEOREMS_PER_BATCH = 10

MAX_RETRIES = 4
SLEEP_BETWEEN_LOOPS = 1

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

# ============================================================
# ENV
# ============================================================

load_dotenv()

# ============================================================
# CLIENT CACHE
# ============================================================

_model_lock = threading.Lock()
_client_cache: dict[str, Any] = {}

SYSTEM_PROMPT = """
You are an expert mathematician specializing in:
- Abstract Algebra
- Group Theory
- Ring Theory
- Field Theory
- Elementary Number Theory

You generate mathematically correct, mutation-friendly theorems.

Your outputs MUST:
- Be undergraduate-level
- Use precise mathematical language
- Separate hypotheses clearly
- Avoid theorem duplicates
- Avoid advanced research-level theorems
- Produce STRICT VALID JSON ONLY
- Never output markdown
- Never output explanations
"""

def _get_client() -> Any:
    """
    Thread-safe Gen AI client cache.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY missing in .env"
        )

    if api_key in _client_cache:
        return _client_cache[api_key]

    with _model_lock:
        if api_key not in _client_cache:
            _client_cache[api_key] = genai.Client(api_key=api_key)

    return _client_cache[api_key]

# ============================================================
# DATASET HELPERS
# ============================================================

def load_dataset(path: str) -> list[dict]:

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_dataset(data: list[dict], path: str):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )


def theorem_names(data: list[dict]) -> set[str]:

    names = set()

    for theorem in data:

        name = theorem.get("name", "").strip()

        if name:
            names.add(name.lower())

    return names

# ============================================================
# PROMPT
# ============================================================

def build_prompt(previous_names: set[str]) -> str:

    # Avoid prompt explosion
    previous_names_list = list(previous_names)[-60:]

    avoid_text = ", ".join(previous_names_list)

    return f"""
Generate {THEOREMS_PER_BATCH} DISTINCT mathematical theorems.

Allowed domains:
- GroupTheory
- RingTheory
- FieldTheory
- NumberTheory

STRICTLY AVOID THESE THEOREMS:
{avoid_text}

Output format MUST be STRICT JSON:

[
  {{
    "id": "unique_string_id",
    "name": "Common theorem name",
    "domain": "GroupTheory",
    "original_full_statement": "Full theorem statement",
    "hypotheses": [
      "Hypothesis 1",
      "Hypothesis 2"
    ],
    "conclusion": "The conclusion"
  }}
]

Requirements:
- Theorems must be standard undergraduate-level theorems.
- Hypotheses must be clearly separable.
- Removing a hypothesis should usually make the theorem false.
- Counterexamples should ideally be computable in Python/SymPy.
- Avoid duplicates.
- Avoid near-duplicates.
- Avoid vague statements.
- Output ONLY raw JSON.
""".strip()

# ============================================================
# GEMINI CALL
# ============================================================

def generate_batch(prompt: str) -> str:

    client = _get_client()
    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3-flash-preview",
    )

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.6,
            max_output_tokens=16384,
            candidate_count=1,
            response_mime_type="application/json",
        ),
    )

    return response.text

# ============================================================
# JSON EXTRACTION
# ============================================================

JSON_ARRAY_REGEX = re.compile(
    r"\[\s*{.*}\s*\]",
    re.DOTALL,
)

def extract_json(text: str):

    text = text.strip()

    # Remove markdown wrappers
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    text = text.strip()

    try:
        return json.loads(text)

    except Exception:
        pass

    match = JSON_ARRAY_REGEX.search(text)

    if not match:
        raise ValueError(
            "Could not locate JSON array in response."
        )

    return json.loads(match.group(0))

# ============================================================
# VALIDATION
# ============================================================

REQUIRED_KEYS = {
    "id",
    "name",
    "domain",
    "original_full_statement",
    "hypotheses",
    "conclusion",
}

VALID_DOMAINS = {
    "GroupTheory",
    "RingTheory",
    "FieldTheory",
    "NumberTheory",
}

def normalize_theorem(theorem: dict) -> dict | None:

    if not isinstance(theorem, dict):
        return None

    missing = REQUIRED_KEYS - theorem.keys()

    if missing:
        return None

    if theorem["domain"] not in VALID_DOMAINS:
        return None

    if not isinstance(theorem["hypotheses"], list):
        return None

    theorem["id"] = theorem.get(
        "id",
        str(uuid.uuid4()),
    )

    theorem["name"] = theorem["name"].strip()

    theorem["hypotheses"] = [
        str(h).strip()
        for h in theorem["hypotheses"]
    ]

    theorem["conclusion"] = theorem[
        "conclusion"
    ].strip()

    theorem["original_full_statement"] = theorem[
        "original_full_statement"
    ].strip()

    return theorem

# ============================================================
# MAIN
# ============================================================

def main():

    dataset = load_dataset(OUTPUT_FILE)

    existing_names = theorem_names(dataset)

    logger.info(
        f"Loaded {len(dataset)} existing theorems."
    )

    loops = 0

    pbar = tqdm(total=TARGET_THEOREMS)
    pbar.update(len(dataset))

    while (
        len(dataset) < TARGET_THEOREMS
        and loops < MAX_LOOPS
    ):

        loops += 1

        logger.info(f"Loop {loops}")

        prompt = build_prompt(existing_names)

        success = False

        for retry in range(MAX_RETRIES):

            try:

                raw = generate_batch(prompt)

                parsed = extract_json(raw)

                if not isinstance(parsed, list):
                    raise ValueError(
                        "Response is not a list."
                    )

                added = 0

                for theorem in parsed:

                    theorem = normalize_theorem(theorem)

                    if theorem is None:
                        continue

                    name_key = theorem["name"].lower()

                    if name_key in existing_names:
                        continue

                    existing_names.add(name_key)

                    dataset.append(theorem)

                    added += 1

                save_dataset(dataset, OUTPUT_FILE)

                logger.info(
                    f"Added {added} theorems "
                    f"(total={len(dataset)})"
                )

                pbar.n = len(dataset)
                pbar.refresh()

                success = True
                break

            except Exception as exc:

                logger.warning(
                    f"Retry {retry + 1} failed: {exc}"
                )

                time.sleep((retry+1) * SLEEP_BETWEEN_LOOPS * 1.5)

        if not success:
            logger.error(
                "Failed batch after retries."
            )

        time.sleep(SLEEP_BETWEEN_LOOPS)

    pbar.close()

    logger.info(
        f"Finished with {len(dataset)} theorems."
    )


if __name__ == "__main__":
    main()