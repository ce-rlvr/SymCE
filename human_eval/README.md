# Human evaluation of generated counterexamples

This folder contains the annotations from our manual study of model-generated
counterexamples, scored against the per-theorem symbolic verifiers.

## Why we judge *outputs*, not *verifier code*

Our first instinct was to human-audit the generated verifier modules directly.
We abandoned that: the verifiers routinely rely on heuristics and finite
simplifications to decide the conditions, and the code can be intricate. Direct
judgement of verifier correctness was therefore slow, difficult, and largely
subjective.

Instead we audit the **end-to-end decision**: we take a sample of counterexamples
emitted by the trained models on the test split and, for each, a human decides
whether the model's witness is *actually* a valid counterexample - independently
of what the verifier concluded. Comparing the human verdict against the verifier
verdict lets a single study bound four separate concerns at once:

1. **Verifier trustworthiness** - do the automatically generated verifiers accept
   good witnesses and reject bad ones?
2. **Hypothesis-drop reliability** - is the mutated conjecture genuinely false?
3. **Reward hacking** - is the model satisfying the verifier without producing a
   real counterexample?
4. **Witness-schema quality** - is the DeepSeek-written witness-schema description
   (how to phrase a witness for a given theorem) accurate enough for the model?

## Sampling

The examples were drawn across multiple seeds and training configurations (SFT,
dense RLVR, sparse RLVR). The sample is split by the *verifier's* verdict:

| File | Verifier verdict | Rows |
|---|---|---|
| `accepted_counterexamples_review.csv` | accepted (scored correct) | 101 |
| `rejected_counterexamples_review.csv` | rejected (scored incorrect) | 76 |
| **Total** | | **177** |

> Note on counts: the paper rounds this study to *176* examples (100 accepted +
> 76 rejected). The released CSVs contain **177** rows (**101** accepted + 76
> rejected); the extra row is a genuine additional accepted-set annotation. The
> numbers below are computed directly from the released CSVs.

Model-type composition of the sample: Dense 85, Sparse 61, SFT 31.

## Columns

`accepted_counterexamples_review.csv`

- `Verifier` - `<theorem_id>__<dropped_hypothesis>` identifying the verifier module
  under `data/verifiers/<Category>/`.
- `Category` - mathematical domain.
- `Accept?` - human verdict: is this a *genuinely valid* counterexample? (`Yes`/`No`)
- `Counterexample` - the witness the model emitted.
- `Results Path` - provenance: the eval-suite run the sample was taken from.
- `Model Type` - Dense / Sparse (/ SFT).
- `Comments` - annotator notes.

`rejected_counterexamples_review.csv` has the same columns, with the human-verdict
column named `Accepted Counterexample?` and no separate `Counterexample` column.

## Findings

### Accepted set (verifier said *correct*) - 101 rows

- **99 / 101** were confirmed by the human as genuinely valid counterexamples.
- **2 / 101** were judged *not* valid despite the verifier accepting them:
  - `thm_center_of_p_group_nontrivial__h1` (Sparse) - the remaining hypotheses hold
    but the conclusion is not actually negated (`neg_Q` not satisfied).
  - `no_proper_algebraic_extensions_of_closed_fields__h1` (FieldTheory, Sparse) - the
    field construction is malformed (one must use `Q(√2)` rather than `2`).

### Rejected set (verifier said *incorrect*) - 76 rows

- **74 / 76** the model's output was indeed wrong - the verifier's rejection was
  correct.
- **2 / 76** the verifier was wrong to reject, and in neither case is the verifier
  module itself at fault:
  - `bw_seq_rn__h3` - **witness-schema description bug (not a verifier bug).** The
    witness the model produced was a valid counterexample, but the DeepSeek-written
    witness schema showed a `Matrix` object used directly, whereas the verifier
    expected it imported from and called as `sympy.Matrix`. The mismatch is in the
    schema *description*, not in the verifier's logic.
  - `word_problem_direct_product` - **not a verification problem: the conjecture was
    still true.** After dropping a hypothesis the theorem remained true, and the
    model correctly emitted `NONE`. The verifier "rejected" only because a
    counterexample was expected where none exists. Theorem details:
    - Original: *"If G and H are finitely generated groups with solvable word
      problems, then their direct product G x H has a solvable word problem."*
    - Dropped hypothesis (`h1`): *"G is a finitely generated group."*
    - Remaining: G has a solvable word problem; H is a finitely generated group; H
      has a solvable word problem.
    - Conclusion: the direct product G x H has a solvable word problem.

## Takeaway

Across the 177 audited examples, only **1** case (`word_problem_direct_product`)
was clearly a conjecture that remained *true* after the hypothesis drop, and only
**1** case (`bw_seq_rn__h3`) was clearly caused by an inaccurate witness-schema
description. No example in the study was traced to an incorrect verifier module.
This bounds the failure modes attributable to the automatic verifier-generation
and hypothesis-dropping pipeline to well under 2% of audited cases.
