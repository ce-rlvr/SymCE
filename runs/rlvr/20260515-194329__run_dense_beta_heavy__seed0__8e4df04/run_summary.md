# RLVR run — 20260515-194329__run_dense_beta_heavy__seed0__8e4df04

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

- **final_reward_mean**: -0.29603582605719564
- **final_kl**: 0.8923165988922119

## Rollouts

- **total**: 4800
- **mean_reward**: -0.2663
- **format_ok_rate**: 0.9877
- **parse_ok_rate**: 0.55
- **q_neg_rate**: 0.1444
- **group_std_pos_rate**: 0.8425
- **plan_p4_group_std_gate_pass**: True
- **reason_counts**:
    - `hyp_only`: 496
    - `oracle_parse_error`: 2101
    - `partial`: 1451
    - `neg_q_only`: 315
    - `success`: 378
    - `no_tag`: 59
