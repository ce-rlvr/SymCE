# Eval suite — thesis_full

- **Elapsed**: 85451.1 s  •  **Cells**: 48
- **Models**: qwen-sft, qwen-rlvr, qwen-rlvr-sparse
- **Benchmarks**: gsm8k, math, aime2024, mmlu_college_math
- **Pass@k**: [1, 3, 5, 8]

## Per-benchmark domain sizes

### gsm8k

| Domain | N |
| --- | ---: |
| `arithmetic` | 1319 |

### math

| Domain | N |
| --- | ---: |
| `Algebra` | 124 |
| `Intermediate Algebra` | 97 |
| `Prealgebra` | 82 |
| `Number Theory` | 62 |
| `Precalculus` | 56 |
| `Geometry` | 41 |
| `Counting & Probability` | 38 |

### aime2024

| Domain | N |
| --- | ---: |
| `AIME` | 30 |

### mmlu_college_math

| Domain | N |
| --- | ---: |
| `college_math` | 100 |

## Results table (mean over problems)

| Model | Benchmark | Style | Pass@1 (greedy) | Pass@1 (sampled) | Pass@3 | Pass@5 | Pass@8 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `qwen-rlvr` | `aime2024` | `standard_cot` | 0.067 | 0.071 | 0.113 | 0.138 | 0.167 |
| `qwen-rlvr` | `aime2024` | `v2_counterexample` | 0.167 | 0.104 | 0.159 | 0.195 | 0.233 |
| `qwen-rlvr` | `gsm8k` | `standard_cot` | 0.880 | 0.879 | 0.948 | 0.963 | 0.973 |
| `qwen-rlvr` | `gsm8k` | `v2_counterexample` | 0.889 | 0.881 | 0.943 | 0.958 | 0.967 |
| `qwen-rlvr` | `math` | `standard_cot` | 0.654 | 0.650 | 0.740 | 0.766 | 0.786 |
| `qwen-rlvr` | `math` | `v2_counterexample` | 0.604 | 0.584 | 0.693 | 0.721 | 0.740 |
| `qwen-rlvr` | `mmlu_college_math` | `standard_cot` | 0.680 | 0.719 | 0.869 | 0.913 | 0.940 |
| `qwen-rlvr` | `mmlu_college_math` | `v2_counterexample` | 0.740 | 0.731 | 0.882 | 0.919 | 0.940 |
| `qwen-rlvr-sparse` | `aime2024` | `standard_cot` | 0.100 | 0.071 | 0.101 | 0.117 | 0.133 |
| `qwen-rlvr-sparse` | `aime2024` | `v2_counterexample` | 0.067 | 0.113 | 0.212 | 0.273 | 0.333 |
| `qwen-rlvr-sparse` | `gsm8k` | `standard_cot` | 0.873 | 0.872 | 0.943 | 0.957 | 0.964 |
| `qwen-rlvr-sparse` | `gsm8k` | `v2_counterexample` | 0.888 | 0.883 | 0.945 | 0.957 | 0.964 |
| `qwen-rlvr-sparse` | `math` | `standard_cot` | 0.662 | 0.630 | 0.733 | 0.760 | 0.780 |
| `qwen-rlvr-sparse` | `math` | `v2_counterexample` | 0.604 | 0.573 | 0.695 | 0.725 | 0.746 |
| `qwen-rlvr-sparse` | `mmlu_college_math` | `standard_cot` | 0.680 | 0.694 | 0.876 | 0.917 | 0.930 |
| `qwen-rlvr-sparse` | `mmlu_college_math` | `v2_counterexample` | 0.730 | 0.731 | 0.893 | 0.936 | 0.960 |
| `qwen-sft` | `aime2024` | `standard_cot` | 0.067 | 0.042 | 0.076 | 0.087 | 0.100 |
| `qwen-sft` | `aime2024` | `v2_counterexample` | 0.067 | 0.029 | 0.074 | 0.104 | 0.133 |
| `qwen-sft` | `gsm8k` | `standard_cot` | 0.791 | 0.768 | 0.917 | 0.943 | 0.958 |
| `qwen-sft` | `gsm8k` | `v2_counterexample` | 0.710 | 0.688 | 0.910 | 0.946 | 0.963 |
| `qwen-sft` | `math` | `standard_cot` | 0.552 | 0.541 | 0.700 | 0.747 | 0.780 |
| `qwen-sft` | `math` | `v2_counterexample` | 0.282 | 0.232 | 0.410 | 0.479 | 0.530 |
| `qwen-sft` | `mmlu_college_math` | `standard_cot` | 0.500 | 0.549 | 0.817 | 0.903 | 0.960 |
| `qwen-sft` | `mmlu_college_math` | `v2_counterexample` | 0.480 | 0.525 | 0.801 | 0.887 | 0.940 |
