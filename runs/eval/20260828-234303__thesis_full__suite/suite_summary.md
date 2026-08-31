# Eval suite — thesis_full

- **Elapsed**: 21271.9 s  •  **Cells**: 18
- **Models**: gemma3-base, gemma3-sft, gemma3-rlvr-dense
- **Benchmarks**: counterexample, theorem_truth
- **Pass@k**: [1, 3, 5, 8]

## Per-benchmark domain sizes

### counterexample

| Domain | N |
| --- | ---: |
| `GroupTheory` | 74 |
| `RingTheory` | 47 |
| `NumberTheory` | 33 |
| `LinearAlgebra` | 20 |
| `FieldTheory` | 14 |
| `RealAnalysis` | 13 |

### theorem_truth

| Domain | N |
| --- | ---: |
| `GroupTheory` | 96 |
| `RingTheory` | 71 |
| `NumberTheory` | 58 |
| `LinearAlgebra` | 45 |
| `FieldTheory` | 39 |
| `RealAnalysis` | 38 |

## Results table (mean over problems)

| Model | Benchmark | Style | Pass@1 (greedy) | Pass@1 (sampled) | Pass@3 | Pass@5 | Pass@8 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `gemma3-base` | `counterexample` | `v2_counterexample` | 0.214 | 0.180 | 0.305 | 0.361 | 0.403 |
| `gemma3-base` | `theorem_truth` | `truth_classify` | 0.536 | 0.528 | 0.765 | 0.833 | 0.867 |
| `gemma3-base` | `theorem_truth` | `v2_counterexample` | 0.473 | 0.425 | 0.707 | 0.819 | 0.902 |
| `gemma3-rlvr-dense` | `counterexample` | `v2_counterexample` | 0.338 | 0.336 | 0.432 | 0.460 | 0.488 |
| `gemma3-rlvr-dense` | `theorem_truth` | `truth_classify` | 0.568 | 0.583 | 0.816 | 0.879 | 0.919 |
| `gemma3-rlvr-dense` | `theorem_truth` | `v2_counterexample` | 0.225 | 0.254 | 0.495 | 0.617 | 0.718 |
| `gemma3-sft` | `counterexample` | `v2_counterexample` | 0.214 | 0.195 | 0.349 | 0.412 | 0.458 |
| `gemma3-sft` | `theorem_truth` | `truth_classify` | 0.017 | 0.038 | 0.106 | 0.166 | 0.242 |
| `gemma3-sft` | `theorem_truth` | `v2_counterexample` | 0.003 | 0.003 | 0.009 | 0.014 | 0.020 |
