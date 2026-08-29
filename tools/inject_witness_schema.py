import os
import json
import argparse
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm


def _normalize_path(path_value: str | None) -> str:
    if not path_value:
        return ""
    try:
        return str(Path(path_value).expanduser().resolve())
    except Exception:
        return str(Path(path_value).expanduser())


def _load_records_file(records_file: str) -> list[dict]:
    records: list[dict] = []
    with open(records_file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                continue
    return records


def _extract_filepaths_from_records(records: list[dict]) -> list[str]:
    filepaths: list[str] = []
    for rec in records:
        v = rec.get("verifier") or {}
        module_path = v.get("module_path") or rec.get("verifier_module_path") or rec.get("module_path")
        if module_path:
            filepaths.append(_normalize_path(module_path))
    return filepaths


def _replace_existing_schema_block(content: str, schema: str) -> str:
    escaped = schema.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
    schema_line = f'WITNESS_SCHEMA = "{escaped}"'
    pattern = re.compile(r"(?ms)^\s*WITNESS_SCHEMA\s*=\s*.*?(?:\n|$)")
    cleaned = pattern.sub("", content).rstrip()
    if cleaned:
        return f"{cleaned}\n\n{schema_line}\n"
    return f"{schema_line}\n"


def _write_jsonl(path: str | Path, records: list[dict]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=True) + "\n")


def _append_jsonl_record(path: str | Path, record: dict) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=True) + "\n")

PROMPT_TEMPLATE = """You are an expert in SymPy and algebraic counterexamples.

Your task is to inspect a single Python verifier module and produce a terse structural witness specification (WITNESS_SCHEMA) that helps a small language model emit a syntactically valid witness object.

Guidelines (must follow):
- The schema is ONLY a structural typing/syntax hint. It is NOT a theorem explanation. It is NOT a counterexample strategy.
- Inspect top-level objects, imports, and the `conditions(witness)` function. If the module exposes a `setup_namespace()` function, prefer the objects it creates; otherwise use top-level names (e.g. `S3`, `I2`, `ZZ`, `eye(2)`).
- Do NOT reveal or hint at any actual witness values, dropped-hypothesis text, or test-case-specific data.
- Do NOT name internal verifier constants like `NEG_Q_INDEX`, `CONDITION_LABELS`, or `N_HYP` in the schema.
- Produce a single human-readable string describing ONE canonical Python object structure (exact container shape + element types + constructors). The schema must not describe multiple valid structures.
- Any example snippets must illustrate only container syntax and object constructors, not mathematical intent or special values.
- DO NOT enumerate or invent symbolic instances (e.g. S3, D4, Z4). If group objects are needed, refer only to their constructor APIs.
- AVOID exhaustive namespace listings.
- Optionally include a SHORT list of relevant imported constructors/types if they are useful and directly used in the module (e.g. SymmetricGroup, DihedralGroup, Matrix, eye, zeros).
- Do NOT enumerate all imports from the module.
- Assume the small model will only see the generated schema string. Therefore the schema must be fully self-contained in structure description, but MUST NOT assume knowledge of any predefined symbolic constants unless explicitly written in the schema.
- Note that the module code and variables will NOT be visible to the small language model. In fact, it wouldn't even recognize the word "module" or "verifier"

Good schema characteristics:
- low entropy
- strongly typed
- concrete
- syntactic
- locally actionable

Few-shot SymPy-flavoured examples (do not leak values; only show types/syntax):

Example 1:
WITNESS_SCHEMA: "Python tuple: (PermutationGroup, PermutationGroup) constructed via SymPy group constructors (e.g. SymmetricGroup(n), DihedralGroup(n)). Example syntax: (SymmetricGroup(3), DihedralGroup(4))"

Example 2:
WITNESS_SCHEMA: "Python tuple (L_basis, S, x_mat):
(list[sympy.Matrix], sympy.Matrix, sympy.Matrix).
Example syntax:
([Matrix([[1,0],[0,1]])], eye(1), Matrix([[0]]))"

Example 3 (field size):
WITNESS_SCHEMA: "A tuple (n, q) where `n` is a positive int (dimension) and `q` is a positive int (prime power). Example form: (3, 7)"

Example 4 (CRT style):
WITNESS_SCHEMA: "Python dict with keys:
'm' -> list[int]
'a' -> list[int]
'M' -> int
'c' -> int.
Example form: {'m': [3,5], 'a':[1,2], 'M':15, 'c':10}"

Example 5:
WITNESS_SCHEMA: "A SymPy Set object (e.g., Interval or FiniteSet) whose convex_hull is non-compact; return as a module Set object or as `Interval(a, b)` if domain objects exist."

Example 6 (function witness):
WITNESS_SCHEMA: "A SymPy expression `f` or a tuple `(f, X)` where `f` is a `sympy` expression and `X` is the domain (e.g., `S.Reals` or `FiniteSet(...)`)."

Example 7:
WITNESS_SCHEMA: "A tuple (R, a, b) where `R` is a ring-like object exposing `elements`, `add`, `mul` and `a,b` are members from `R.elements`."

Now, given the verifier module source, inspect the module and produce ONLY a JSON object on stdout with this exact shape (no extra text):
{"WITNESS_SCHEMA": "<concise schema string>"}

The schema string should be short. Use SymPy type names when possible. Include a 1-line example snippet showing how the witness should be structured (using constructor-based syntax when applicable) is highly recommended as long as it follows the guidelines.

Rules:
- Output valid JSON only.
- Do not use markdown.
- Do not output explanations.
\n+Verifier module source (verbatim):
{verifier_code}
"""


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _call_llm(client, model_name, prompt):
    return client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful mathematical AI producing strict JSON."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
        response_format={"type": "json_object"}
    )

def process_file(args):
    file_path, api_key, model_name, write_inplace = args
    if not file_path.endswith('.py'):
        return {"file": file_path, "status": "skipped", "reason": "not_py"}

    with open(file_path, 'r') as f:
        content = f.read()

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    prompt = PROMPT_TEMPLATE.replace("{verifier_code}", content)

    try:
        response = _call_llm(client, model_name, prompt)
        # response.choices[0].message.content may be either a JSON string or dict-like
        content_resp = None
        try:
            content_resp = response.choices[0].message.content
        except Exception:
            content_resp = str(response)

        # Ensure we have a JSON string
        if isinstance(content_resp, dict):
            data = content_resp
        else:
            data = json.loads(content_resp)

        schema = data.get("WITNESS_SCHEMA", "")

        if not schema:
            print(f"No schema returned for {file_path}; skipping")
            return {"file": file_path, "status": "skipped", "reason": "empty_schema"}

        if write_inplace:
            rewritten = _replace_existing_schema_block(content, schema)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(rewritten)

            print(f"Injected into {file_path}")

        return {
            "file": file_path,
            "module_path": _normalize_path(file_path),
            "status": "ok",
            "schema": schema,
            "injected": write_inplace,
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {"file": file_path, "status": "error", "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Generate witness-schema JSONL sidecars for verifier modules using DeepSeek/OpenAI-compatible API.")
    parser.add_argument('--dir', type=str, default=os.path.join(os.getcwd(), 'data', 'verifiers'), help='Directory to walk for verifier .py files')
    parser.add_argument('--records-file', type=str, default=None, help='Optional JSONL v2 file (e.g. data/algebra_counterexamples_v2.jsonl) to extract verifier.module_path entries from')
    parser.add_argument('--max-records', type=int, default=0, help='If >0, limit the number of verifier files processed (applies after dedup)')
    parser.add_argument('--workers', type=int, default=8, help='Number of concurrent API workers')
    parser.add_argument('--model', type=str, default=None, help='Override model name (falls back to DEEPSEEK_MODEL env var)')
    parser.add_argument('--output-jsonl', type=str, default=os.path.join(os.getcwd(), 'data', 'witness_schemas.jsonl'), help='Output JSONL file for generated schemas (overwritten by default)')
    parser.add_argument('--merged-output-jsonl', type=str, default=None, help='Optional JSONL file that copies the input records and adds witness_schema to each record')
    parser.add_argument('--inplace', action='store_true', help='Rewrite verifier files with a WITNESS_SCHEMA constant for legacy compatibility')
    parser.add_argument('--no-inplace', action='store_true', help='Explicitly disable in-place rewriting')
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    model_name = args.model or os.environ.get('DEEPSEEK_MODEL', 'deepseek-v4-flash')

    if not api_key:
        print("Error: DEEPSEEK_API_KEY not set in environment or .env")
        return

    existing_schemas = {}
    if args.output_jsonl and os.path.exists(args.output_jsonl):
        try:
            existing_records = _load_records_file(args.output_jsonl)
            for r in existing_records:
                mp = r.get("module_path") or r.get("file")
                if mp and r.get("schema"):
                    existing_schemas[_normalize_path(mp)] = r["schema"]
            print(f"Loaded {len(existing_schemas)} existing schemas from {args.output_jsonl}")
        except Exception as e:
            print(f"Failed to load existing schemas: {e}")

    filepaths = []
    records_for_merge: list[dict] = []

    # If a records JSONL is provided, extract module paths from each record's verifier.module_path
    if args.records_file:
        try:
            records_for_merge = _load_records_file(args.records_file)
            filepaths.extend(_extract_filepaths_from_records(records_for_merge))
        except FileNotFoundError:
            print(f"Records file not found: {args.records_file}")
            return

    # Fallback: walk the directory
    if not filepaths:
        for root, dirs, files in os.walk(args.dir):
            for f in files:
                if f.endswith('.py'):
                    filepaths.append(os.path.join(root, f))

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for p in filepaths:
        norm_p = _normalize_path(p)
        if norm_p not in seen and norm_p not in existing_schemas:
            seen.add(norm_p)
            deduped.append(norm_p)

    if args.max_records and args.max_records > 0:
        deduped = deduped[:args.max_records]

    print(f"Processing {len(deduped)} verifier files (workers={args.workers}, model={model_name})")

    write_inplace = bool(args.inplace) and not bool(args.no_inplace)
    tasks = [(f, api_key, model_name, write_inplace) for f in deduped]

    results: list[dict] = []

    if args.output_jsonl:
        Path(args.output_jsonl).parent.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {executor.submit(process_file, task): task[0] for task in tasks}
        for future in tqdm(as_completed(future_map), total=len(future_map), desc="Extracting schemas"):
            result = future.result()
            if not result:
                continue
            results.append(result)
            if result.get("status") == "ok" and args.output_jsonl:
                _append_jsonl_record(args.output_jsonl, result)

    ok_results = [result for result in results if result.get("status") == "ok"]
    if args.output_jsonl:
        print(f"Updated schema sidecar at {args.output_jsonl}")

    if args.merged_output_jsonl and args.records_file:
        schema_map = {
            _normalize_path(result.get("module_path") or result.get("file")): result.get("schema", "")
            for result in ok_results
            if result.get("schema")
        }
        merged_records: list[dict] = []
        for rec in records_for_merge:
            merged = dict(rec)
            verifier = merged.get("verifier") or {}
            for candidate in (
                merged.get("witness_schema"),
                schema_map.get(_normalize_path(verifier.get("module_path"))),
                schema_map.get(_normalize_path(merged.get("verifier_module_path"))),
                schema_map.get(_normalize_path(merged.get("module_path"))),
            ):
                if candidate:
                    merged["witness_schema"] = candidate
                    break
            merged_records.append(merged)
        _write_jsonl(args.merged_output_jsonl, merged_records)
        print(f"Wrote merged records to {args.merged_output_jsonl}")


if __name__ == '__main__':
    main()