# RLVR run — 20260514-125057__run_sparse_pilot__seed0__fdd3542

## Configuration

- **config_yaml**: configs/run_sparse_pilot.yaml
- **seed**: 0
- **sft_checkpoint**: runs/sft/20260513-223721__full_run__seed42__da490c1/lora
- **train_jsonl**: data/rlvr_prompts_v2.jsonl
- **reward_mode**: oracle
- **task_mode**: counterexample_only
- **oracle_reward_weights**:
    - `alpha`: 0.0
    - `beta`: 1.0
    - `gamma`: 0.0
    - `delta`: 0.0
    - `epsilon`: 1.0
- **num_generations**: 4
- **max_steps**: 30
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.22708333333333333
- **final_kl**: 0.7653110941251119

## Rollouts

- **total**: 960
- **mean_reward**: -0.2271
- **format_ok_rate**: 0.9969
- **parse_ok_rate**: 0.5844
- **q_neg_rate**: 0.1885
- **group_std_pos_rate**: 0.6833
- **plan_p4_group_std_gate_pass**: False
- **reason_counts**:
    - `hyp_only`: 99
    - `success`: 97
    - `partial`: 281
    - `oracle_parse_error`: 396
    - `neg_q_only`: 84
    - `no_tag`: 3
