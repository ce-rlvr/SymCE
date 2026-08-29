# RLVR run — 20260515-050321__run_dense_beta_heavy__seed0__fdd3542

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
- **max_steps**: 80
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.27385416875282925
- **final_kl**: 0.9333245318072537

## Rollouts

- **total**: 2560
- **mean_reward**: -0.2636
- **format_ok_rate**: 0.9945
- **parse_ok_rate**: 0.5422
- **q_neg_rate**: 0.1473
- **group_std_pos_rate**: 0.7781
- **plan_p4_group_std_gate_pass**: True
- **reason_counts**:
    - `hyp_only`: 259
    - `oracle_parse_error`: 1158
    - `partial`: 752
    - `neg_q_only`: 162
    - `success`: 215
    - `no_tag`: 14
