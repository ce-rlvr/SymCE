# RLVR run - 20260521-112140__full_run_dense_test__seed42__db0287f

## Configuration

- **config_yaml**: configs/full_run_dense_test.yaml
- **seed**: 42
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260520-060436__full_run__seed42__638156c/lora
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

- **final_loss**: 0.02912776470184326
- **final_reward_mean**: 0.401293040615403
- **final_kl**: 0.42659934028051794

## Rollouts

- **mean_reward**: 0.2437
- **format_ok_rate**: 0.9654
- **parse_ok_rate**: 0.7871
- **q_neg_rate**: 0.386
- **group_std_pos_rate**: 0.6627
