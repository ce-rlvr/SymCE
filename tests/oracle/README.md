# Verifier audit suite

`verifier_unit_tests.jsonl` is the hand-curated suite that `tools/verifier_audit.py`
runs against `data/symce_corpus.jsonl` (the production
v2 corpus) to gate the trustworthiness of the Gemini-generated verifier modules.

PLAN Section P1.5 calls for >=50 entries, >=5 per algebra subdomain, with the gate set
at >=90 % per-domain pass rate before any P6-grade RLVR launch.

## Schema

Each JSONL line is a test record:

```json
{
  "theorem_id": "abelian_direct_product",
  "dropped_hypothesis_name": "h1",
  "witness_expr": "(CyclicGroup(2), CyclicGroup(3))",
  "expected_all_pass": false,
  "expected_conditions": [true, false],
  "notes": "Free-form justification - useful when reviewing a failure."
}
```

- `expected_all_pass: true`  => verifier returns all-`True` conditions.
- `expected_all_pass: false` => at least one condition must be `False`. If
  `expected_conditions` is also present, the verifier output must match it
  byte-for-byte (stronger than "at least one False"). Prefer the explicit form
  whenever you can write down the expected pattern; it tests the verifier's
  *discriminative* power, not just its happy-path arithmetic.

## Coverage (current draft)

| Domain        | Positive | Targeted negative | Total |
| ---           | ---      | ---               | ---   |
| GroupTheory   | 9        | 3                 | 12    |
| RingTheory    | 7        | 0                 | 7     |
| FieldTheory   | 7        | 0                 | 7     |
| LinearAlgebra | 9        | 1                 | 10    |
| NumberTheory  | 3        | 1                 | 4     |
| RealAnalysis  | 8        | 0                 | 8     |
| **Total**     | **43**   | **5**             | **48** |

**Known gaps (please extend before P6 launch):**
- NumberTheory has only 3 records in the reconstructed corpus with
  `witness_passes_verifier=True`; only 4 NumberTheory audit cases are
  authorable from the current corpus. Either (a) extend the v2 corpus with
  more NumberTheory hypothesis-drops, or (b) author NumberTheory tests
  against verifier modules on disk that aren't currently linked from the v2
  JSONL (those tests would require a `--allow-disk-verifier` extension to the
  audit tool - not yet implemented).
- RingTheory / FieldTheory currently have no targeted-negative cases.
  Counterexample-discriminative tests in these domains require careful
  algebra (constructing a witness that satisfies the remaining hypotheses
  but accidentally lands on the *correct* conclusion). Recommended next:
  - `prime_artinian_is_simple/h2`: try a field like `QQ` -> Artinian and
    simple, should produce `[True, False]`.
  - `bezout_identity_polynomials/h3`: try coprime polynomials like
    `(QQ, x-1, x+1)` -> gcd=1, so neg_Q should be False, giving `[True, True, False]`.
- The audit tool does not currently support testing for *expected parse
  errors* (e.g. "witness `None` should be rejected"). Tests of that shape
  would need a small extension (`expected_parse_ok: false`); skipped for now.

## Running the audit

```bash
# Against the production v2 corpus (reconstructed)
python -m tools.verifier_audit \
    --v2-jsonl  data/symce_corpus.jsonl \
    --suite     tests/oracle/verifier_unit_tests.jsonl \
    --report    data/verifier_audit_report.json

# Against the dev-sample (legacy, smaller corpus)
python -m tools.verifier_audit
```

Exit code is `0` when every algebra-domain pass rate clears 90 % and `1`
otherwise - wire that into CI before P6.
