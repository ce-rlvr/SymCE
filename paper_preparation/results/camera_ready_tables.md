# Camera-ready tables

Regenerated from raw evaluation records by `paper_preparation/scripts/build_camera_ready_tables.py`.

Theorem-truth `v2_counterexample` uses **strict** scoring (literal NONE sentinel only); the lenient variant is shown for comparison.

## In-domain counterexample benchmark (reference seed 42, n=201)

| Model | Pass@1 greedy | Pass@8 sampled | Conclusion-pass | Format-OK | Parse-OK |
|---|---:|---:|---:|---:|---:|
| base | 0.303 | 0.483 | 0.303 | 0.45 | 0.42 |
| SFT | 0.348 | 0.637 | 0.413 | 1.00 | 0.82 |
| dense | 0.502 | 0.677 | 0.612 | 0.98 | 0.94 |
| sparse | 0.497 | 0.672 | 0.592 | 0.97 | 0.95 |

## Theorem-truth probe (reference seed 42, n=347)

| Model | v2 strict | v2 as shipped | truth_classify | says FALSE | no verdict |
|---|---:|---:|---:|---:|---:|
| base | 0.271 | 0.865 | 0.357 | 0.026 | 0.617 |
| SFT | 0.000 | 0.000 | 0.210 | 0.703 | 0.086 |
| dense | 0.343 | 0.372 | 0.729 | 0.239 | 0.032 |
| sparse | 0.654 | 0.686 | 0.839 | 0.150 | 0.012 |

## Four-seed robustness (seeds 42, 19, 31, 64)

| Metric | base | SFT | dense | sparse |
|---|---:|---:|---:|---:|
| counterexample_pass_at_1_greedy | 0.303 | 0.342 +/- 0.015 | 0.485 +/- 0.022 | 0.463 +/- 0.025 |
| counterexample_pass_at_8_sampled | 0.486 | 0.619 +/- 0.020 | 0.660 +/- 0.020 | 0.641 +/- 0.022 |
| truth_v2_strict | 0.271 | 0.000 +/- 0.000 | 0.333 +/- 0.041 | 0.659 +/- 0.044 |
| truth_classify | 0.357 | 0.161 +/- 0.045 | 0.706 +/- 0.086 | 0.747 +/- 0.133 |

Sparse minus dense on the v2 probe: **0.326 +/- 0.083**, per seed 42=0.311, 19=0.421, 31=0.352, 64=0.222.

## Out-of-domain transfer (mean over seeds 42, 19, 31, 64)

| Benchmark | n | base | SFT | dense | sparse |
|---|---:|---:|---:|---:|---:|
| gsm8k | 1319 | 0.830 | 0.815 +/- 0.030 | 0.876 +/- 0.019 | 0.880 +/- 0.014 |
| math | 500 | 0.130 | 0.550 +/- 0.015 | 0.653 +/- 0.016 | 0.649 +/- 0.009 |
| mmlu_college_math | 100 | 0.340 | 0.538 +/- 0.029 | 0.703 +/- 0.052 | 0.718 +/- 0.041 |
| aime2024 | 30 | 0.000 | 0.067 +/- 0.027 | 0.075 +/- 0.032 | 0.075 +/- 0.017 |

Seeds without transfer evaluations: .

## Reason distribution (reference seed 42, greedy, n=201)

| Model | hyp_only | neg_q_only | no_tag | none_on_false | oracle_parse_error | partial | success |
|---|---|---|---|---|---|---|---|
| base | 0.010 | 0.000 | 0.547 | 0.085 | 0.035 | 0.020 | 0.303 |
| SFT | 0.308 | 0.065 | 0.005 | 0.000 | 0.174 | 0.100 | 0.348 |
| dense | 0.214 | 0.109 | 0.020 | 0.020 | 0.040 | 0.095 | 0.502 |
| sparse | 0.189 | 0.095 | 0.035 | 0.100 | 0.015 | 0.070 | 0.498 |

## Per-domain Pass@1 (reference seed 42, greedy)

| Domain | n | base | SFT | dense | sparse |
|---|---:|---:|---:|---:|---:|
| GroupTheory | 74 | 0.257 | 0.338 | 0.500 | 0.473 |
| RingTheory | 47 | 0.277 | 0.255 | 0.489 | 0.468 |
| NumberTheory | 33 | 0.485 | 0.515 | 0.545 | 0.606 |
| LinearAlgebra | 20 | 0.300 | 0.450 | 0.550 | 0.600 |
| FieldTheory | 14 | 0.286 | 0.286 | 0.500 | 0.357 |
| RealAnalysis | 13 | 0.231 | 0.231 | 0.385 | 0.462 |

## External comparators (n=201)

| Model | Pass@1 greedy | Pass@8 sampled |
|---|---:|---:|
| eurus-2-7b-prime | 0.298 | 0.567 |
| qwen25-math-7b-instruct | 0.199 | 0.289 |
| deepseek-math-7b-rl | 0.104 | 0.308 |
| abel-7b-002 | 0.045 | 0.224 |
| mammoth2-7b-plus | 0.000 | 0.219 |
| qwen-base | 0.010 | 0.095 |
| gemini-flash-lite | 0.577 | 0.687 |
| gemini-flash | 0.492 | -- |
| gemini-flash-preview | 0.468 | 0.771 |
| deepseek-pro | 0.428 | 0.622 |
| gemini-pro | 0.433 | -- |
| deepseek-flash | 0.423 | 0.637 |

Commercial-API greedy Pass@1 range across 6 models: **0.423 to 0.577**.

## Gemma-3-4B replication

| Run | Arm | Pass@1 | Pass@8 | truth_classify | v2 strict |
|---|---|---:|---:|---:|---:|
| seed56 | base | 0.214 | 0.403 | 0.490 | 0.398 |
| seed24 | base | 0.214 | 0.403 | 0.490 | 0.398 |
| seed24 | sft | 0.214 | 0.458 | 0.003 | 0.000 |
| seed24 | dense | 0.338 | 0.488 | 0.539 | 0.216 |

Gemma RLVR v2-probe results are not reported; those checkpoints and their configs are not part of the artifact release.

## Human audit of verifier decisions

- Audited decisions: **177** (101 accepted, 76 rejected)
- Accepted and confirmed valid: **99/101** (false-accept rate 0.020)
- Rejected and confirmed invalid: **74/76**
- Overall decision accuracy: **0.9774**

## Excluded runs

- `20260714-043917` - single exploratory LoRA rank-64 SFT probe; not part of the reported configuration
