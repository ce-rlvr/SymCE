# RLVR run — 20260514-131007__run_sparse_pilot__seed0__fdd3542

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
- **max_steps**: -1
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.9251644736842105
- **final_kl**: 0.32414968547068146

## Rollouts

- **total**: 14016
- **mean_reward**: -0.5898
- **format_ok_rate**: 0.5745
- **parse_ok_rate**: 0.3268
- **q_neg_rate**: 0.0834
- **group_std_pos_rate**: 0.5334
- **plan_p4_group_std_gate_pass**: False
- **reason_counts**:
    - `hyp_only`: 892
    - `success`: 613
    - `partial`: 2512
    - `oracle_parse_error`: 3472
    - `neg_q_only`: 556
    - `no_tag`: 5964
    - `none_on_false`: 7
