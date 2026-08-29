# RLVR run - 20260706-225550__64_full_run_dense__seed64__6e33172

## Configuration

- **config_yaml**: configs/seeds/64_full_run_dense.yaml
- **seed**: 64
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260706-221950__64_full_run_dense__seed64__6e33172/lora
- **train_jsonl**: data/rlvr_prompts_v2.jsonl
- **reward_mode**: oracle
- **task_mode**: counterexample_only
- **oracle_reward_weights**:
    - `alpha`: 0.25
    - `beta`: 0.65
    - `gamma`: 0.1
    - `delta`: 0.3
    - `epsilon`: 1.0
- **num_generations**: 4
- **beta**: 0.02

## Training

- **final_loss**: 0.04406650066375732
- **final_reward_mean**: 0.3800057863506178
- **final_kl**: 0.29442560815045404

## Rollouts

- **mean_reward**: 0.261
- **format_ok_rate**: 0.9633
- **parse_ok_rate**: 0.8017
- **q_neg_rate**: 0.3857
- **group_std_pos_rate**: 0.6523
