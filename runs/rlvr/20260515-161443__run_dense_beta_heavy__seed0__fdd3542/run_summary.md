# RLVR run — 20260515-161443__run_dense_beta_heavy__seed0__fdd3542

## Configuration

- **config_yaml**: configs/run_dense_beta_heavy.yaml
- **seed**: 0
- **sft_checkpoint**: runs/sft/20260513-223721__full_run__seed42__da490c1/lora
- **train_jsonl**: data/rlvr_prompts_v2.jsonl
- **reward_mode**: oracle
- **task_mode**: counterexample_only
- **oracle_reward_weights**:
    - `alpha`: 0.1
    - `beta`: 0.8
    - `gamma`: 0.1
    - `delta`: 0.5
    - `epsilon`: 1.0
- **num_generations**: 4
- **max_steps**: 200
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.3789229193329811
- **final_kl**: 0.6950393998622895

## Rollouts

- **total**: 6400
- **mean_reward**: -0.2869
- **format_ok_rate**: 0.9523
- **parse_ok_rate**: 0.5309
- **q_neg_rate**: 0.1347
- **group_std_pos_rate**: 0.78
- **plan_p4_group_std_gate_pass**: True
- **reason_counts**:
    - `hyp_only`: 659
    - `success`: 469
    - `partial`: 1876
    - `oracle_parse_error`: 2697
    - `neg_q_only`: 393
    - `no_tag`: 305
    - `none_on_false`: 1
