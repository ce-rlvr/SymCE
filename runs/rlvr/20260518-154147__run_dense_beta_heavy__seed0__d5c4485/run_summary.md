# RLVR run — 20260518-154147__run_dense_beta_heavy__seed0__d5c4485

## Configuration

- **config_yaml**: configs/run_dense_beta_heavy.yaml
- **seed**: 0
- **sft_checkpoint**: runs/sft/20260517-215205__full_run__seed42__d5c4485/lora
- **train_jsonl**: data/rlvr_prompts_v2.jsonl
- **reward_mode**: oracle
- **task_mode**: counterexample_only
- **oracle_reward_weights**:
    - `alpha`: 0.1
    - `beta`: 0.8
    - `gamma`: 0.1
    - `delta`: 0.5
    - `epsilon`: 1.0
- **num_generations**: 8
- **max_steps**: -1
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.9722411793011886
- **final_kl**: 0.2694539720049271

## Rollouts

- **total**: 28032
- **mean_reward**: -0.9014
- **format_ok_rate**: 0.1504
- **parse_ok_rate**: 0.0799
- **q_neg_rate**: 0.0255
- **group_std_pos_rate**: 0.5223
- **plan_p4_group_std_gate_pass**: False
- **reason_counts**:
    - `oracle_parse_error`: 1977
    - `hyp_only`: 539
    - `success`: 391
    - `partial`: 974
    - `neg_q_only`: 323
    - `no_tag`: 23815
    - `none_on_false`: 13
