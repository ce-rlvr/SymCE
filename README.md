# SymCE

**Counterexample generation against per-theorem symbolic verifiers.**

[Paper](https://aclanthology.org/2026.findings-emnlp.2112/) ·
[arXiv](https://arxiv.org/abs/2610.02444) ·
[Project page](https://ce-rlvr.github.io/SymCE/) ·
[Dataset](https://huggingface.co/datasets/ce-rlvr/SymCE)

SymCE is a corpus of **4,707 false** undergraduate algebra and real-analysis
conjectures. Each one is a true theorem with a single hypothesis removed, and
each comes with an **executable Python verifier** and a one-line *witness
schema* describing what an acceptable counterexample looks like. A verifier
runs in about 130 ms, so the same check serves as the reward during
reinforcement learning: SymCE is a training environment, not only a benchmark.

This repository accompanies *Counterexample Generation via Per-Theorem Symbolic
Verifiers: When Imitation Hurts and Reinforcement Repairs* (Findings of EMNLP
2026) and reproduces every number in it.

**Main finding.** Fine-tuning Qwen3-4B on counterexamples alone drops its
recognition of true theorems from 0.27 to 0.00. RL against the verifiers with a
sparse, outcome-only reward restores it to 0.66. A dense reward with partial
credit reaches the same counterexample success rate but only 0.33 on true
theorems.

---

## The task

Given a false conjecture "if `H1 and ... and Hk` then `Q`", emit a witness `w`
such that every remaining hypothesis holds on `w` and `Q` fails on `w`. The
policy writes one Python expression; the verifier returns one boolean per
remaining hypothesis plus one for the negated conclusion:

```python
>>> from src.oracle.sandbox import run_oracle
>>> run_oracle("data/verifiers/GroupTheory/abelian_direct_product__h1.py",
...            "(SymmetricGroup(3), CyclicGroup(2))", n_conditions=2).conditions
[True, True]      # the remaining hypothesis holds and the conclusion is negated
```

The theorem says that the direct product of two abelian groups is abelian.
Without "G is abelian" it is false, and S3 paired with C2 is a witness.
Evaluation runs in a sandboxed subprocess with a hard timeout, and no language
model judges the answer. A model may also answer `NONE`, meaning that no
counterexample exists. Whether it keeps that option is what the paper is about.

---

## Quick start

```bash
git clone https://github.com/ce-rlvr/SymCE && cd SymCE
pip install -r requirements.txt
python -m pytest tests                              # oracle, sandbox and reward tests
python tools/verify_corpus_integrity.py --sums      # check the shipped splits
```

The splits are also on the Hugging Face Hub:

```python
from datasets import load_dataset
test = load_dataset("ce-rlvr/SymCE", "test")["test"]
```

---

## Repository layout

| Path | Contents |
|---|---|
| `data/` | The corpus, the splits and the 12,376 verifier modules (see `data/README.md`) |
| `src/` | Oracle, sandbox and verifier loader |
| `training/` | SFT, GRPO/RLVR and the evaluation suite runner |
| `configs/` | All training and evaluation configurations, including every seed |
| `prompts/` | The verifier-generation and witness-extraction teacher prompts, as used |
| `human_eval/` | The 177-decision human audit and its annotations |
| `runs/eval/` | Per-record evaluation outputs for every suite the paper cites |
| `results_summary/` | Training curves and rollout summaries for the reported runs |
| `paper_preparation/` | Analysis scripts, the tables they generate, and the figures |
| `hf_release/` | Builders for the Hugging Face dataset and model repositories |
| `tools/` | Corpus construction, split building and maintenance scripts |
| `tests/` | Oracle, sandbox and reward unit tests |
| `docs/` | The project page, served by GitHub Pages |

### Splits

| File | n | Purpose |
|---|---:|---|
| `data/test_set.jsonl` | 201 | Held-out counterexample benchmark |
| `data/sft_data.jsonl` | 1,000 | Supervised fine-tuning |
| `data/rlvr_prompts.jsonl` | 3,506 | RLVR prompt set |
| `data/theorem_truth_eval.jsonl` | 347 | Calibration probe of **true** theorems |

Splits are stratified by domain with a fixed seed (42), independent of the
training seed. The six domains are group, ring, number and field theory, linear
algebra and real analysis. Exact counts are in `data/dataset_stats.json`.

Verifier paths inside the records are repo-relative
(`data/verifiers/<Domain>/<theorem_id>__<hyp>.py`), so the oracle runs from a
fresh clone. `python tools/normalise_verifier_paths.py --check` exits non-zero
if an absolute path has crept back in.

### Names in the paper and in the data

The paper calls the two prompt styles *SymCE-prompt* and *truth-classify*. In
the records and in `configs/eval/` the first is `v2_counterexample`, the
identifier the evaluation harness has always used. The outcome labels map as
follows:

| Paper | Records |
|---|---|
| success | `success` |
| not-Q only | `neg_q_only` |
| abstain | `none_on_false` |
| hyp-only | `hyp_only` |
| partial | `partial` |
| parse error | `oracle_parse_error` |
| no tag | `no_tag` |

Archived run records under `runs/` and `results_summary/` refer to the split
files by their original names (`test_set_v2.jsonl` and so on). They are kept
exactly as the runs wrote them.

---

## Reproducing the paper

Every table is regenerated from the raw per-record evaluation outputs by one
script. Nothing is transcribed by hand.

```bash
python -m paper_preparation.scripts.build_camera_ready_tables \
    --runs-root runs --audit-dir human_eval \
    --out-dir paper_preparation/results
```

This writes `camera_ready_tables.{json,md}`: the in-domain benchmark, the
calibration probes, the four-seed robustness summary, out-of-domain transfer,
the outcome taxonomy, the per-domain breakdown, the external comparators and the
human audit.

Related analyses, which read the gzipped per-cell outputs in `runs/eval/`:

```bash
python -m paper_preparation.scripts.bootstrap_cis        # 95% bootstrap CIs
python -m paper_preparation.scripts.eval_reason_dist     # outcome counts per model
python -m paper_preparation.scripts.make_plots --all     # figures
```

`bootstrap_cis` emits one row per (model, seed, benchmark, metric). The figure
script pins the reference seed (42). `eval_reason_dist` keeps the most recent
suite for each model, so for the trained Qwen models its output is not the
reference seed; the outcome taxonomy reported in the paper is the one in
`camera_ready_tables.md`.

### Answer extraction

The evaluation harness originally fell back, when a completion had no answer
frame, to matching any bare *true* or *false* anywhere in the text. In a chain
of thought about whether a theorem is true, that word appears constantly, so
completions that ran out of tokens mid-reasoning were scored as if they had
answered. This inflated **untrained baselines** in particular; trained models
emit the required format and are barely affected.

`paper_preparation/scripts/truth_answer.py` replaces that parser, and
`build_camera_ready_tables.py` rescores both calibration probes from the raw
completions. The paper reports the corrected numbers and gives the original
ones alongside. The module docstrings document the evidence.

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

The verifiers are written by a teacher model, so their reliability was measured
rather than assumed. We audit the quantity that carries the reward signal, the
accept/reject **decision** on real policy outputs, rather than the verifier
source, which relies on heuristics and finite simplifications that make a
judgement of the code largely subjective.

177 decisions were checked by hand: **99/101** accepted witnesses were genuinely
valid (2.0% false-accept rate) and **74/76** rejections were correct, for
**97.7%** decision accuracy. No case was traced to an incorrect verifier module.
The annotations, including the four disputed decisions, are in `human_eval/`.

---

## Integrity

`data/SHA256SUMS` holds the hash of every released split:

```bash
python tools/verify_corpus_integrity.py --sums
python tools/verify_corpus_integrity.py --against-rev $(git rev-list --max-parents=0 HEAD)
```

The second form compares each split with the first commit while ignoring the
verifier-path fields, which shows that rewriting those paths changed nothing
else in any of the 13,090 records.

The training runs under `runs/sft/` and `runs/rlvr/` recorded their input hashes
in `status.json` at launch. Those records predate the path rewrite, so they do
not match the current files byte for byte; the check above shows that only the
paths moved.

The evaluation suites wrote an empty `dataset_fingerprint.json`. That was a
defect in `run_suite.py`, now fixed, so new runs record their inputs. The
fourteen archived suites cannot be back-filled honestly, since a hash computed
today would not show what those runs read at the time.

---

## Project page

`docs/` holds a single static page with no build step and no external requests.
GitHub Pages serves it from **Settings, Pages, Deploy from a branch**, with
`main` and the `/docs` folder. To preview it locally:

```bash
python3 -m http.server -d docs 8000
```

The numbers on the page are the four-seed means from
`paper_preparation/results/camera_ready_tables.md`. The social preview image
`docs/static/figures/fig_calibration.png` is generated by
`paper_preparation/scripts/make_calibration_figure.py`.

---

## Not included

**Model weights are not published yet.** The twelve Qwen3-4B LoRA adapters
behind the reported numbers (seeds 42, 19, 31 and 64, each as SFT, RLVR-dense and
RLVR-sparse) will go on the Hub under `ce-rlvr`; `hf_release/README.md` explains
how they are built and uploaded.

The Gemma-3-4B adapters are not distributed. The seed-24 Gemma evaluation
outputs are in `runs/eval/`; the seed-56 outputs are not, so the Gemma row of
Table 5 cannot be regenerated from this repository, while the rest of the paper
can. Base models are downloaded from their original sources.

---

## Citation

```bibtex
@inproceedings{zouak-etal-2026-counterexample,
    title = "Counterexample Generation via Per-Theorem Symbolic Verifiers: When Imitation Hurts and Reinforcement Repairs",
    author = "Zouak, Omar Farouk  and
      Boukhalfa, Houssam Eddine  and
      Lakehal, Soumaya  and
      Katiyar, Shiv  and
      Nefti-Meziani, Samia",
    editor = "Lee, Hung-Yi  and
      Dev, Sunipa  and
      Li, Jessy  and
      Elliott, Desmond",
    booktitle = "Findings of the {A}ssociation for {C}omputational {L}inguistics: {EMNLP} 2026",
    month = oct,
    year = "2026",
    address = "Budapest, Hungary",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.findings-emnlp.2112/",
    pages = "45032--45047",
    ISBN = "979-8-89176-462-0",
}
```

## Licence

Code is MIT (`LICENSE`). The corpus, verifier modules, witness schemas and audit
annotations are CC BY 4.0 (`LICENSE-DATA`).
