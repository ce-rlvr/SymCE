# SymCE

**Counterexample generation against per-theorem symbolic verifiers.**

SymCE is a corpus of **4,707 false** undergraduate algebra and real-analysis
conjectures. Each one is produced by dropping a single hypothesis from a true
theorem, and each is paired with an **independent, executable Python verifier**
and a one-line *witness schema* describing the shape of an acceptable
counterexample.

Because a verifier runs in about 130 ms, the same substrate serves as the reward
function during reinforcement learning. SymCE is therefore a **training
environment**, not only an evaluation benchmark.

This repository accompanies *Counterexample Generation via Per-Theorem Symbolic
Verifiers: When Imitation Hurts and Reinforcement Repairs* (Findings of EMNLP
2026) and reproduces every number in it.

---

## The task

Given a false conjecture of the form "if `H₁ ∧ … ∧ H_k` then `Q`", emit a witness
`w` such that every remaining hypothesis holds on `w` and `Q` fails on `w`. The
policy emits a one-line Python expression; the verifier returns one boolean per
remaining hypothesis plus one for the negated conclusion:

```python
>>> from src.oracle.sandbox import run_oracle
>>> run_oracle("data/verifiers/GroupTheory/abelian_direct_product__h1.py",
...            "(SymmetricGroup(3), CyclicGroup(2))", n_conditions=2).conditions
[True, True]      # remaining hypothesis holds; the conclusion is negated
```

The theorem states that the direct product of two abelian groups is abelian;
dropping "G is abelian" makes it false, and `S₃ × C₂` witnesses that. Evaluation
happens in a sandboxed subprocess with a hard timeout.

A model may also answer `NONE`, asserting that no counterexample exists. Getting
that judgement right is what the paper is about.

---

## What is here

| Path | Contents |
|---|---|
| `data/` | The corpus, the splits, and 12,376 verifier modules |
| `src/` | Oracle, sandbox, verifier loader |
| `training/` | SFT, GRPO/RLVR, and the evaluation suite runner |
| `configs/` | Every training and evaluation configuration, including all four seeds |
| `prompts/` | The verifier-generation and witness-extraction teacher prompts |
| `human_eval/` | The 177-decision human audit and its annotations |
| `runs/eval/` | Per-record evaluation outputs for every suite the paper cites |
| `paper_preparation/` | The analysis scripts and their generated tables |
| `results_summary/` | Training curves and rollout summaries for the reported runs |

### Splits

| Split | n | Purpose |
|---|---:|---|
| `data/test_set_v2.jsonl` | 201 | Held-out counterexample benchmark |
| `data/sft_data_v2.jsonl` | 1,000 | Supervised fine-tuning |
| `data/rlvr_prompts_v2.jsonl` | 3,506 | RLVR prompt set |
| `data/theorem_truth_eval.jsonl` | 347 | Calibration probe — **true** theorems |

Splits are stratified by domain with a fixed seed. The corpus spans Group
Theory, Ring Theory, Number Theory, Linear Algebra, Field Theory and Real
Analysis; see `data/dataset_stats_v2.json` for exact counts.

---

## Reproducing the paper

Every table is regenerated from the raw per-record evaluation outputs by a single
script. Nothing is transcribed by hand.

```bash
pip install -r requirements.txt
python paper_preparation/scripts/build_camera_ready_tables.py \
    --runs-root runs --audit-dir human_eval \
    --out-dir paper_preparation/results
```

This writes `camera_ready_tables.{json,md}`, covering the in-domain benchmark,
the calibration probes, the four-seed robustness summary, out-of-domain
transfer, the reason taxonomy, the per-domain breakdown, the external
comparators and the human audit.

Related analyses:

```bash
python -m paper_preparation.scripts.bootstrap_cis        # 95% bootstrap CIs
python -m paper_preparation.scripts.eval_reason_dist     # reason taxonomy
python -m paper_preparation.scripts.make_plots --all     # figures
```

### A note on answer extraction

The evaluation harness originally fell back, when a completion contained no
answer frame, to matching any bare occurrence of the word *true* or *false*
anywhere in the text. In a chain of thought about whether a theorem is true that
word occurs constantly, so completions that ran out of tokens mid-reasoning were
scored as if they had answered. This inflated **untrained baselines** in
particular — trained models emit the required format and are barely affected.

`paper_preparation/scripts/truth_answer.py` replaces that parser, and
`build_camera_ready_tables.py` rescores both calibration probes from the raw
completions. The paper reports the corrected numbers and gives the original ones
alongside. See the module docstrings for the evidence.

---

## Training

Both stages run on a single 32 GB consumer GPU. SFT takes under five minutes;
each RLVR run takes about nine hours.

```bash
python -m training.sft.train  --config configs/full_run_dense.yaml
python -m training.rlvr.train --config configs/full_run_dense.yaml   # dense reward
python -m training.rlvr.train --config configs/full_run_sparse.yaml  # sparse reward
```

The two configurations differ **only** in the reward weights. Additional seeds
are in `configs/seeds/`.

---

## Verifier reliability

Verifiers are generated by a teacher model, so their reliability has to be
established rather than assumed. We audit the quantity that actually carries the
reward signal — the accept/reject **decision** on real policy outputs — rather
than the verifier source, which relies on heuristics and finite simplifications
that make a judgement on the code itself largely subjective.

177 decisions were checked by hand: **99/101** accepted witnesses were confirmed
genuinely valid (2.0 % false-accept rate) and **74/76** rejections were confirmed
correct, for **97.7 %** decision accuracy. No case was traced to an incorrect
verifier module. The annotations, including the four disputed decisions, are in
`human_eval/`.

---

## Not included

Gemma-3-4B adapters, training configurations and evaluation outputs are not part
of this release, so the Gemma results reported in the paper are not reproducible
from it. Everything reported for Qwen3-4B is.

Model weights are not distributed. Base models are downloaded from their original
sources; adapters are available on request.

---

## Licence

Code is MIT (`LICENSE`). The corpus, verifier modules, witness schemas and audit
annotations are CC BY 4.0 (`LICENSE-DATA`).

## Citation

See `CITATION.cff`.
