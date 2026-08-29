# RLVR run — 20260513-234459__full_run__seed0__96b730b

## Configuration

- **config_yaml**: configs/full_run.yaml
- **seed**: 0
- **sft_checkpoint**: runs/sft/20260513-223721__full_run__seed42__da490c1/lora
- **train_jsonl**: data/rlvr_prompts_v2.jsonl
- **reward_mode**: oracle
- **task_mode**: counterexample_only
- **oracle_reward_weights**:
    - `alpha`: 0.25
    - `beta`: 0.6
    - `gamma`: 0.1
    - `delta`: 0.5
    - `epsilon`: 1.0
- **num_generations**: 8
- **max_steps**: -1
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.053595752777675025
- **final_kl**: 0.7838642780597394

## Rollouts

- **total**: 28032
- **mean_reward**: -0.3229
- **format_ok_rate**: 0.8
- **parse_ok_rate**: 0.549
- **q_neg_rate**: 0.0902
- **group_std_pos_rate**: 0.0
- **plan_p4_group_std_gate_pass**: False
- **reason_counts**:
    - `hyp_only`: 1757
    - `success`: 1339
    - `partial`: 10315
    - `oracle_parse_error`: 7036
    - `neg_q_only`: 1190
    - `no_tag`: 5606
    - `none_on_false`: 789
