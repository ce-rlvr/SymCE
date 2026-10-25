# The SymCE corpus

4,707 false conjectures over 3,485 distinct undergraduate theorems, each paired
with an executable verifier and a witness schema.

## How it was built

| Stage | Count |
|---|---:|
| Source theorems, structured into hypotheses + conclusion | 6,748 |
| Candidate drops, one per `(theorem, hypothesis)` pair | 18,262 |
| Candidates for which the teacher produced a verifier module | 12,376 |
| **Records retained after gating** | **4,707** |
| - of which the canonical witness passed at generation time (*strict pool*) | 2,389 |
| - valid verifier, no oracle-confirmed canonical witness (*loose pool*) | 2,318 |
| Distinct theorems covered | 3,485 |
| Records carrying a witness schema | 4,700 |

A candidate is retained only if the teacher model (Gemini 3.1 Pro) classifies the
mutated statement as well-posed and non-trivial, emits a valid Python verifier,
proposes a counterexample, and that counterexample evaluates to `True` on its own
verifier without execution errors. Up to five retries with error-trace feedback
are allowed. Witness schemas are written post hoc by a second teacher (DeepSeek)
from the verifier source and its canonical witness.

## Files

| File | Rows | Description |
|---|---:|---|
| `symce_corpus.jsonl` | 4,707 | The full corpus |
| `test_set.jsonl` | 201 | Held-out benchmark, domain-stratified |
| `sft_data.jsonl` | 1,000 | Supervised fine-tuning split |
| `rlvr_prompts.jsonl` | 3,506 | RLVR prompt set |
| `theorem_truth_eval.jsonl` | 347 | Calibration probe - **true** theorems, never mutated |
| `witness_schemas.jsonl` | 4,676 | One-line witness-shape descriptions, one per verifier module (covering 4,700 records) |
| `dataset_stats.json` | - | Per-domain counts and token statistics |
| `oracle_perf_probe.json` | - | Verifier latency measurements |
| `verifiers/<Domain>/<theorem_id>__<hypothesis>.py` | 12,376 | The verifier modules |

## Record shape

```json
{
  "theorem_id": "abelian_direct_product",
  "dropped_hypothesis_name": "h1",
  "domain": "GroupTheory",
  "remaining_hypotheses": ["H is an abelian group"],
  "conclusion": "G x H is abelian",
  "witness_schema": "Python tuple (G, H) of sympy PermutationGroup objects...",
  "canonical_witness": "(SymmetricGroup(3), CyclicGroup(2))"
}
```

## Verifier contract

Each module exposes `conditions(witness) -> list[bool]`, returning one boolean
per remaining hypothesis followed by one for the negated conclusion. A witness
counts as a counterexample when every entry is `True`.

The policy and the verifier share no code path beyond Python's `eval`. Verifiers
are compiled once and reused across all rollouts for that conjecture, so the
reward signal cannot drift during training.

The evaluation namespace is strict about imports: a witness must use
`sympy.Matrix` rather than a bare `Matrix`. Some rejections in the human audit
were mathematically sound witnesses that violated this, which means reported
Pass@1 is a lower bound on mathematical ability.

## Theorem-truth probe

`theorem_truth_eval.jsonl` holds 347 **true** theorems drawn from the same
source, used to measure whether a model can still recognise a true statement
after being trained to produce counterexamples. Each record carries a `subset`
field: `extra_stratified` (n=150) if the theorem's *mutated* form appeared in
RLVR training, `from_test_set` (n=197) if it did not. Reporting the two
separately bounds memorisation.

## Scope

Mutations are single-hypothesis drops only. This is deliberate - it gives every
false conjecture a known, attributable cause of falsity, which is what makes the
per-hypothesis boolean interface possible - but it means the corpus does not span
conclusion mutation, multi-hypothesis dropping, or AST-level mutation. Verifier
coverage is bounded by what is decidable in Python with SymPy and Z3.

## Licence

CC BY 4.0. See `../LICENSE-DATA`.
