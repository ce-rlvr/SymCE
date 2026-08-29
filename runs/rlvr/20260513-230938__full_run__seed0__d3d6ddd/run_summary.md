# RLVR run — 20260513-230938__full_run__seed0__d3d6ddd

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
- **max_steps**: 10
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.4035416718572378
- **final_kl**: 0.8360573790967465

## Rollouts

- **total**: 80
- **mean_reward**: -0.4035
- **format_ok_rate**: 1.0
- **parse_ok_rate**: 0.4875
- **q_neg_rate**: 0.05
- **group_std_pos_rate**: 0.0
- **plan_p4_group_std_gate_pass**: False
- **reason_counts**:
    - `hyp_only`: 6
    - `partial`: 29
    - `oracle_parse_error`: 41
    - `neg_q_only`: 4
