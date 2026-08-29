# RLVR run — 20260519-115727__run_dense_beta_heavy__seed0__019b8bc

## Configuration

- **config_yaml**: configs/run_dense_beta_heavy.yaml
- **seed**: 0
- **sft_checkpoint**: runs/sft/20260518-232341__full_run__seed42__013dcad/lora
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

- **final_reward_mean**: 0.09334414996779881
- **final_kl**: 0.18286573772247022

## Rollouts

- **total**: 28032
- **mean_reward**: -0.0102
- **format_ok_rate**: 0.9158
- **parse_ok_rate**: 0.7016
- **q_neg_rate**: 0.3123
- **group_std_pos_rate**: 0.915
- **plan_p4_group_std_gate_pass**: True
- **reason_counts**:
    - `hyp_only`: 4084
    - `oracle_parse_error`: 6004
    - `partial`: 3720
    - `success`: 6015
    - `neg_q_only`: 2738
    - `no_tag`: 2360
    - `none_on_false`: 3111
