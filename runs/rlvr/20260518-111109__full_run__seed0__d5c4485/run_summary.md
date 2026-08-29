# RLVR run — 20260518-111109__full_run__seed0__d5c4485

## Configuration

- **config_yaml**: configs/full_run.yaml
- **seed**: 0
- **sft_checkpoint**: runs/sft/20260517-215205__full_run__seed42__d5c4485/lora
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

- **final_reward_mean**: -0.30345052452041554
- **final_kl**: 0.37190953814066374

## Rollouts

- **total**: 28032
- **mean_reward**: -0.6463
- **format_ok_rate**: 0.4532
- **parse_ok_rate**: 0.2509
- **q_neg_rate**: 0.0785
- **group_std_pos_rate**: 0.6835
- **plan_p4_group_std_gate_pass**: False
- **reason_counts**:
    - `oracle_parse_error`: 5672
    - `hyp_only`: 1685
    - `success`: 1174
    - `partial`: 3113
    - `neg_q_only`: 1026
    - `no_tag`: 15328
    - `none_on_false`: 34
