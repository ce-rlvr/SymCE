import json
import logging
import os
import re
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from tqdm import tqdm

# ============================================================
# CONFIG
# ============================================================

OUTPUT_FILE = "synthetic_theorems_v2.json"

TARGET_THEOREMS = 10_000
THEOREMS_PER_BATCH = 10

TOPIC_LOOPS = 8

MAX_RETRIES = 3
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
- Linear Algebra
- Real Analysis
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
""".strip()


def _get_client() -> Any:
    """
    Thread-safe Gen AI client cache.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing in .env")

    if api_key in _client_cache:
        return _client_cache[api_key]

    with _model_lock:
        if api_key not in _client_cache:
            _client_cache[api_key] = genai.Client(api_key=api_key)

    return _client_cache[api_key]


# ============================================================
# TOPICS
# ============================================================

@dataclass(frozen=True)
class TopicSpec:
    name: str
    domain: str


TOPICS: list[TopicSpec] = [
    # Group Theory
    TopicSpec("Sylow p-subgroups", "GroupTheory"),
    TopicSpec("Solvable groups", "GroupTheory"),
    TopicSpec("Nilpotent groups", "GroupTheory"),
    TopicSpec("Free groups", "GroupTheory"),
    TopicSpec("Permutation and alternating groups", "GroupTheory"),
    TopicSpec("Automorphism groups", "GroupTheory"),
    TopicSpec("Direct products of groups", "GroupTheory"),
    TopicSpec("Semidirect products of groups", "GroupTheory"),
    TopicSpec("Group actions and orbits", "GroupTheory"),
    TopicSpec("Stabilizers and orbit-stabilizer", "GroupTheory"),
    TopicSpec("Conjugacy classes", "GroupTheory"),
    TopicSpec("Normal subgroups and quotients", "GroupTheory"),
    TopicSpec("Group homomorphisms and kernels", "GroupTheory"),
    TopicSpec("Cyclic groups", "GroupTheory"),
    TopicSpec("Abelian groups and structure theorem", "GroupTheory"),
    TopicSpec("Commutator subgroup and derived series", "GroupTheory"),
    TopicSpec("Center of a group", "GroupTheory"),
    TopicSpec("Group presentations", "GroupTheory"),
    TopicSpec("Isomorphism theorems for groups", "GroupTheory"),
    TopicSpec("Cauchy and Lagrange theorems", "GroupTheory"),
    TopicSpec("Class equation", "GroupTheory"),
    TopicSpec("Semisimple finite groups (basic)", "GroupTheory"),

    # Ring Theory
    TopicSpec("Principal ideal domains", "RingTheory"),
    TopicSpec("Unique factorization domains", "RingTheory"),
    TopicSpec("Euclidean domains", "RingTheory"),
    TopicSpec("Noetherian rings", "RingTheory"),
    TopicSpec("Artinian rings", "RingTheory"),
    TopicSpec("Polynomial rings and ideals", "RingTheory"),
    TopicSpec("Boolean rings", "RingTheory"),
    TopicSpec("Local rings", "RingTheory"),
    TopicSpec("Prime and maximal ideals", "RingTheory"),
    TopicSpec("Ring homomorphisms and kernels", "RingTheory"),
    TopicSpec("Quotient rings", "RingTheory"),
    TopicSpec("Chinese remainder theorem for rings", "RingTheory"),
    TopicSpec("Integral domains", "RingTheory"),
    TopicSpec("Nilpotent elements and nilradical", "RingTheory"),
    TopicSpec("Units and group of units", "RingTheory"),
    TopicSpec("Factor rings of polynomial rings", "RingTheory"),
    TopicSpec("Irreducibility criteria in polynomials", "RingTheory"),
    TopicSpec("Gauss lemma and content", "RingTheory"),
    TopicSpec("Localization of rings", "RingTheory"),
    TopicSpec("Product of ideals", "RingTheory"),
    TopicSpec("Primary decomposition (basic)", "RingTheory"),

    # Field / Galois Theory
    TopicSpec("Galois extensions", "FieldTheory"),
    TopicSpec("Finite fields", "FieldTheory"),
    TopicSpec("Algebraic closures", "FieldTheory"),
    TopicSpec("Splitting fields", "FieldTheory"),
    TopicSpec("Cyclotomic fields", "FieldTheory"),
    TopicSpec("Minimal polynomials", "FieldTheory"),
    TopicSpec("Field extensions and degrees", "FieldTheory"),
    TopicSpec("Separable and inseparable extensions", "FieldTheory"),
    TopicSpec("Normal extensions", "FieldTheory"),
    TopicSpec("Galois group actions", "FieldTheory"),
    TopicSpec("Fundamental theorem of Galois theory", "FieldTheory"),

    # Linear Algebra
    TopicSpec("Jordan canonical form", "LinearAlgebra"),
    TopicSpec("Inner product spaces", "LinearAlgebra"),
    TopicSpec("Dual spaces and annihilators", "LinearAlgebra"),
    TopicSpec("Bilinear forms", "LinearAlgebra"),
    TopicSpec("Quadratic forms", "LinearAlgebra"),
    TopicSpec("Orthogonal matrices", "LinearAlgebra"),
    TopicSpec("Unitary matrices", "LinearAlgebra"),
    TopicSpec("Spectral theorem variants", "LinearAlgebra"),
    TopicSpec("Diagonalization criteria", "LinearAlgebra"),
    TopicSpec("Minimal and characteristic polynomials", "LinearAlgebra"),
    TopicSpec("Rank-nullity and linear maps", "LinearAlgebra"),
    TopicSpec("Invariant subspaces", "LinearAlgebra"),
    TopicSpec("Cayley-Hamilton theorem", "LinearAlgebra"),
    TopicSpec("Projection operators", "LinearAlgebra"),
    TopicSpec("Singular value decomposition (basic)", "LinearAlgebra"),

    # Real Analysis / Calculus / Topology
    TopicSpec("Uniform continuity", "RealAnalysis"),
    TopicSpec("Uniform convergence", "RealAnalysis"),
    TopicSpec("Riemann integration bounds", "RealAnalysis"),
    TopicSpec("Lebesgue integration bounds", "RealAnalysis"),
    TopicSpec("Metric spaces and compactness", "RealAnalysis"),
    TopicSpec("Connectedness in topological spaces", "RealAnalysis"),
    TopicSpec("Power series and radius of convergence", "RealAnalysis"),
    TopicSpec("Differentiability in several variables", "RealAnalysis"),
    TopicSpec("Lipschitz continuity", "RealAnalysis"),
    TopicSpec("Heine-Borel theorem", "RealAnalysis"),
    TopicSpec("Mean value theorem variants", "RealAnalysis"),
    TopicSpec("Intermediate value theorem", "RealAnalysis"),
    TopicSpec("Completeness of the real numbers", "RealAnalysis"),
    TopicSpec("Bolzano-Weierstrass theorem", "RealAnalysis"),
    TopicSpec("Arzela-Ascoli (basic)", "RealAnalysis"),

    # Number Theory
    TopicSpec("Congruences and modular arithmetic", "NumberTheory"),
    TopicSpec("Diophantine equations", "NumberTheory"),
    TopicSpec("Quadratic reciprocity", "NumberTheory"),
    TopicSpec("Arithmetic functions", "NumberTheory"),
    TopicSpec("Continued fractions", "NumberTheory"),
    TopicSpec("Chinese remainder theorem in Z", "NumberTheory"),
    TopicSpec("Euler totient properties", "NumberTheory"),
    TopicSpec("Fermat and Euler theorems", "NumberTheory"),
    TopicSpec("Orders modulo n", "NumberTheory"),
    TopicSpec("Prime factorization and gcd", "NumberTheory"),
    TopicSpec("Pythagorean triples", "NumberTheory"),
    TopicSpec("Linear congruences", "NumberTheory"),
    TopicSpec("Legendre and Jacobi symbols", "NumberTheory"),
    TopicSpec("Sum of divisors function", "NumberTheory"),
    TopicSpec("Modular inverses", "NumberTheory"),
]

VALID_DOMAINS = {
    "GroupTheory",
    "RingTheory",
    "FieldTheory",
    "LinearAlgebra",
    "RealAnalysis",
    "NumberTheory",
}

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


def topic_name_map(data: list[dict]) -> dict[str, set[str]]:
    mapping: dict[str, set[str]] = {topic.name: set() for topic in TOPICS}

    for theorem in data:
        name = theorem.get("name", "").strip()
        topic = theorem.get("topic", "").strip()

        if name and topic in mapping:
            mapping[topic].add(name.lower())

    return mapping

# ============================================================
# PROMPT
# ============================================================


def build_prompt(topic: TopicSpec, previous_names: set[str]) -> str:
    # Avoid prompt explosion
    previous_names_list = list(previous_names)[-60:]
    avoid_text = ", ".join(previous_names_list)

    return f"""
Generate {THEOREMS_PER_BATCH} DISTINCT mathematical theorems in the topic: {topic.name}.

Allowed domain: {topic.domain}

STRICTLY AVOID THESE THEOREMS (same topic only):
{avoid_text}

Output format MUST be STRICT JSON:

[
  {{
    "id": "unique_string_id",
    "name": "Common theorem name",
    "domain": "{topic.domain}",
    "topic": "{topic.name}",
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
        "gemini-3.1-pro-preview",
    )

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.65,
            max_output_tokens=65536,
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
        raise ValueError("Could not locate JSON array in response.")

    return json.loads(match.group(0))

# ============================================================
# VALIDATION
# ============================================================

REQUIRED_KEYS = {
    "id",
    "name",
    "domain",
    "topic",
    "original_full_statement",
    "hypotheses",
    "conclusion",
}


def normalize_theorem(theorem: dict, topic: TopicSpec) -> dict | None:
    if not isinstance(theorem, dict):
        return None

    missing = REQUIRED_KEYS - theorem.keys()
    if missing:
        return None

    if theorem.get("domain") not in VALID_DOMAINS:
        return None

    if not isinstance(theorem.get("hypotheses"), list):
        return None

    theorem["id"] = theorem.get("id") or str(uuid.uuid4())
    theorem["name"] = str(theorem.get("name", "")).strip()
    theorem["topic"] = topic.name
    theorem["domain"] = topic.domain

    theorem["hypotheses"] = [str(h).strip() for h in theorem["hypotheses"]]
    theorem["conclusion"] = str(theorem.get("conclusion", "")).strip()
    theorem["original_full_statement"] = str(
        theorem.get("original_full_statement", "")
    ).strip()

    if not theorem["name"] or not theorem["original_full_statement"]:
        return None

    return theorem

# ============================================================
# MAIN
# ============================================================


def main():
    dataset = load_dataset(OUTPUT_FILE)
    existing_names = theorem_names(dataset)
    topic_names = topic_name_map(dataset)

    logger.info(f"Loaded {len(dataset)} existing theorems.")

    total_loops = len(TOPICS) * TOPIC_LOOPS
    pbar = tqdm(total=TARGET_THEOREMS)
    pbar.update(len(dataset))

    loops_run = 0

    for topic in TOPICS:
        for _ in range(TOPIC_LOOPS):
            if len(dataset) >= TARGET_THEOREMS:
                break

            loops_run += 1
            logger.info(
                f"Loop {loops_run}/{total_loops} | Topic: {topic.name}"
            )

            prompt = build_prompt(topic, topic_names.get(topic.name, set()))
            success = False

            raw = None
            for retry in range(MAX_RETRIES):
                try:
                    raw = generate_batch(prompt)
                    parsed = extract_json(raw)

                    if not isinstance(parsed, list):
                        raise ValueError("Response is not a list.")

                    added = 0

                    for theorem in parsed:
                        theorem = normalize_theorem(theorem, topic)

                        if theorem is None:
                            continue

                        name_key = theorem["name"].lower()
                        if name_key in existing_names:
                            continue

                        existing_names.add(name_key)
                        topic_names.setdefault(topic.name, set()).add(name_key)
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
                    if raw is not None:
                        logger.debug(f"Raw response: {raw}")

                    logger.warning(f"Retry {retry + 1} failed: {exc}")
                    time.sleep((retry + 1) * SLEEP_BETWEEN_LOOPS)

            if not success:
                logger.error("Failed batch after retries.")

            time.sleep(SLEEP_BETWEEN_LOOPS)

        if len(dataset) >= TARGET_THEOREMS:
            break

    pbar.close()
    logger.info(f"Finished with {len(dataset)} theorems.")


if __name__ == "__main__":
    main()
