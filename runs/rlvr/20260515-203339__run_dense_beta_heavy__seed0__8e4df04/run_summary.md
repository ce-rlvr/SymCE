# RLVR run — 20260515-203339__run_dense_beta_heavy__seed0__8e4df04

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
- **max_steps**: 150
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.30258749701082704
- **final_kl**: 0.822238587141037

## Rollouts

- **total**: 4800
- **mean_reward**: -0.2733
- **format_ok_rate**: 0.9785
- **parse_ok_rate**: 0.541
- **q_neg_rate**: 0.1369
- **group_std_pos_rate**: 0.7817
- **plan_p4_group_std_gate_pass**: True
- **reason_counts**:
    - `hyp_only`: 531
    - `success`: 364
    - `partial`: 1408
    - `oracle_parse_error`: 2100
    - `neg_q_only`: 293
    - `no_tag`: 103
    - `none_on_false`: 1
