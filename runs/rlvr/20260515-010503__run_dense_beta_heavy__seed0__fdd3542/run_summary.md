# RLVR run — 20260515-010503__run_dense_beta_heavy__seed0__fdd3542

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
- **max_steps**: -1
- **report_to**: wandb

## Training

- **final_reward_mean**: -0.9725603037758878
- **final_kl**: 0.3212806628434919

## Rollouts

- **total**: 14016
- **mean_reward**: -0.6292
- **format_ok_rate**: 0.5081
- **parse_ok_rate**: 0.2766
- **q_neg_rate**: 0.0703
- **group_std_pos_rate**: 0.494
- **plan_p4_group_std_gate_pass**: False
- **reason_counts**:
    - `hyp_only`: 713
    - `success`: 535
    - `partial`: 2161
    - `oracle_parse_error`: 3244
    - `neg_q_only`: 451
    - `no_tag`: 6895
    - `none_on_false`: 17
