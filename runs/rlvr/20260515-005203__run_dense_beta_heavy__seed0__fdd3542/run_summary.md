# RLVR run — 20260515-005203__run_dense_beta_heavy__seed0__fdd3542

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
- **max_steps**: 8
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.23891927488148212
- **final_kl**: 0.8267221136484295

## Rollouts

- **total**: 256
- **mean_reward**: -0.2389
- **format_ok_rate**: 1.0
- **parse_ok_rate**: 0.5508
- **q_neg_rate**: 0.1602
- **group_std_pos_rate**: 0.7812
- **plan_p4_group_std_gate_pass**: True
- **reason_counts**:
    - `hyp_only`: 25
    - `partial`: 75
    - `oracle_parse_error`: 115
    - `neg_q_only`: 14
    - `success`: 27
