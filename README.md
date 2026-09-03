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

| | |
|---|---|
| Project page | https://ce-rlvr.github.io/SymCE/ |
| Dataset | https://huggingface.co/datasets/ce-rlvr/SymCE |
| Models | https://huggingface.co/ce-rlvr (12 LoRA adapters: 4 seeds x SFT / RLVR-dense / RLVR-sparse) |

---

## The task

Given a false conjecture of the form "if `H1 and ... and Hk` then `Q`", emit a
witness `w` such that every remaining hypothesis holds on `w` and `Q` fails on
`w`. The policy emits a one-line Python expression; the verifier returns one
boolean per remaining hypothesis plus one for the negated conclusion:

```python
>>> from src.oracle.sandbox import run_oracle
>>> run_oracle("data/verifiers/GroupTheory/abelian_direct_product__h1.py",
...            "(SymmetricGroup(3), CyclicGroup(2))", n_conditions=2).conditions
[True, True]      # remaining hypothesis holds; the conclusion is negated
```

The theorem states that the direct product of two abelian groups is abelian.
Dropping "G is abelian" makes it false, and the symmetric group S3 paired with
the cyclic group C2 witnesses that. Evaluation happens in a sandboxed subprocess
with a hard timeout.

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
| `results_summary/` | Training curves and rollout summaries for the reported runs |
| `paper_preparation/` | The analysis scripts, their generated tables and the figures |
| `hf_release/` | Builders for the Hugging Face dataset and model repositories |
| `tools/` | Corpus construction, split building and maintenance scripts |
| `tests/` | Oracle, sandbox and reward unit tests |
| `docs/` | Source of the project page, served by GitHub Pages |

### Splits

| Split | n | Purpose |
|---|---:|---|
| `data/test_set.jsonl` | 201 | Held-out counterexample benchmark |
| `data/sft_data.jsonl` | 1,000 | Supervised fine-tuning |
| `data/rlvr_prompts.jsonl` | 3,506 | RLVR prompt set |
| `data/theorem_truth_eval.jsonl` | 347 | Calibration probe, containing **true** theorems |

Splits are stratified by domain with a fixed seed (42), which is independent of
the training seed. The corpus spans Group Theory, Ring Theory, Number Theory,
Linear Algebra, Field Theory and Real Analysis. See `data/dataset_stats.json`
for exact counts and `data/README.md` for the record schema.

Verifier locations inside the JSONL records are repo-relative
(`data/verifiers/<Domain>/<theorem_id>__<hyp>.py`), so the oracle runs from a
fresh checkout. `python tools/normalise_verifier_paths.py --check` verifies this
and exits non-zero if any absolute path has crept back in.

### Names used in the paper and in the data

The paper writes the two prompt styles as *SymCE-prompt* and *truth-classify*.
In the released records and in `configs/eval/`, the first is spelled
`v2_counterexample`, which is the identifier the evaluation harness has always
used. The paper's outcome labels map onto the record fields the same way:
*success*, *not-Q only*, *abstain*, *hyp-only*, *partial*, *parse error* and
*no tag* are stored as `success`, `neg_q_only`, `none_on_false`, `hyp_only`,
`partial`, `oracle_parse_error` and `no_tag`.

Archived run records under `runs/` and `results_summary/` refer to the split
files by their original names (`test_set_v2.jsonl` and so on). Those records are
left exactly as the runs wrote them rather than rewritten to match the new names.

### Integrity

`data/SHA256SUMS` carries the hash of every released split as shipped:

```bash
python tools/verify_corpus_integrity.py --sums
python tools/verify_corpus_integrity.py --against-rev $(git rev-list --max-parents=0 HEAD)
```

The second form compares each split with the first commit while ignoring the
verifier-path fields, which shows that rewriting those paths changed nothing
else in any of the 13,090 records.

The training runs under `runs/sft/` and `runs/rlvr/` recorded their own input
hashes in `status.json` at launch. Those are genuine run-time records, and they
predate the path rewrite, so they will not match the current files byte for
byte; the check above is what establishes that only the paths moved.

The evaluation suites wrote an empty `dataset_fingerprint.json`. That was a
defect in `run_suite.py`, now fixed, so runs made from this revision onward
record their inputs properly. The fourteen archived suites cannot be
back-filled honestly, since a hash computed today would not be evidence of what
those runs read at the time.

---

## Reproducing the paper

Every table is regenerated from the raw per-record evaluation outputs by a single
script. Nothing is transcribed by hand.

```bash
pip install -r requirements.txt
python -m paper_preparation.scripts.build_camera_ready_tables \
    --runs-root runs --audit-dir human_eval \
    --out-dir paper_preparation/results
```

This writes `camera_ready_tables.{json,md}`, covering the in-domain benchmark,
the calibration probes, the four-seed robustness summary, out-of-domain
transfer, the outcome taxonomy, the per-domain breakdown, the external
comparators and the human audit.

Related analyses:

```bash
python -m paper_preparation.scripts.bootstrap_cis        # 95% bootstrap CIs
python -m paper_preparation.scripts.eval_reason_dist     # outcome taxonomy
python -m paper_preparation.scripts.make_plots --all     # figures
```

All four read the gzipped per-cell outputs in `runs/eval/`. `bootstrap_cis`
emits one row per (model, seed, benchmark, metric); the figure script pins the
reference seed so a model evaluated at several seeds cannot be represented by
whichever suite happened to be read last.

### A note on answer extraction

The evaluation harness originally fell back, when a completion contained no
answer frame, to matching any bare occurrence of the word *true* or *false*
anywhere in the text. In a chain of thought about whether a theorem is true that
word occurs constantly, so completions that ran out of tokens mid-reasoning were
scored as if they had answered. This inflated **untrained baselines** in
particular; trained models emit the required format and are barely affected.

`paper_preparation/scripts/truth_answer.py` replaces that parser, and
`build_camera_ready_tables.py` rescores both calibration probes from the raw
completions. The paper reports the corrected numbers and gives the original ones
alongside. See the module docstrings for the evidence.

---

## Training

Both stages run on a single 32 GB consumer GPU. SFT takes under five minutes;
each RLVR run takes about nine hours.

```bash
python -m training.sft.train  --config configs/full_run_dense_better.yaml
python -m training.rlvr.train --config configs/full_run_dense_better.yaml  # dense reward
python -m training.rlvr.train --config configs/full_run_sparse.yaml        # sparse reward
```

The dense and sparse configurations differ **only** in the reward weights.
Additional seeds are in `configs/seeds/`.

The reference-seed runs were launched from `configs/full_run.yaml` (SFT) and
`configs/full_run_dense_test.yaml` (dense RLVR), which the paper cites. Neither
original file survived, so both were reconstructed from the corresponding run's
recorded `config.json` and carry a header saying so. They reproduce the settings
exactly, including the 3 SFT epochs used at seed 42 and the dense reward weights
(0.25, 0.65, 0.10, 0.30, 1.00), but each holds only the section its run used.
Every run directory keeps its own resolved `config.json`, which remains the
authoritative record of what a given number came from.

---

## Verifier reliability

Verifiers are generated by a teacher model, so their reliability has to be
established rather than assumed. We audit the quantity that actually carries the
reward signal, the accept/reject **decision** on real policy outputs, rather
than the verifier source, which relies on heuristics and finite simplifications
that make a judgement on the code itself largely subjective.

177 decisions were checked by hand: **99/101** accepted witnesses were confirmed
genuinely valid (2.0 % false-accept rate) and **74/76** rejections were confirmed
correct, for **97.7 %** decision accuracy. No case was traced to an incorrect
verifier module. The annotations, including the four disputed decisions, are in
`human_eval/`.

---

## The project page

`docs/` holds a single static page with no build step and no external requests.
GitHub Pages serves it from **Settings, Pages, Deploy from a branch**, choosing
`main` and the `/docs` folder. To preview it locally:

```bash
python3 -m http.server -d docs 8000
```

Its three figures are regenerated by `make_plots.py` and
`make_calibration_figure.py`, so the page cannot drift from the reported
numbers.

---

## Not included

The Gemma-3-4B adapters are not distributed. The seed-24 Gemma evaluation
outputs are in `runs/eval/`; the seed-56 outputs are not, so the Gemma row of
Table 5 cannot be regenerated from this repository while the rest of the paper
can.

Base models are downloaded from their original sources. The twelve Qwen3-4B LoRA
adapters behind the reported numbers are on the Hub under
[`ce-rlvr`](https://huggingface.co/ce-rlvr); see `hf_release/README.md` for how
they are built and published.

---

## Licence

Code is MIT (`LICENSE`). The corpus, verifier modules, witness schemas and audit
annotations are CC BY 4.0 (`LICENSE-DATA`).

## Citation

See `CITATION.cff`.
