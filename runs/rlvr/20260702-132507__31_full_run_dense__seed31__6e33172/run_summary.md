# RLVR run - 20260702-132507__31_full_run_dense__seed31__6e33172

## Configuration

- **config_yaml**: configs/seeds/31_full_run_dense.yaml
- **seed**: 31
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260702-124825__31_full_run_dense__seed31__6e33172/lora
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

- **final_loss**: 0.037103623151779175
- **final_reward_mean**: 0.2925509991538193
- **final_kl**: 0.48720810702070594

## Rollouts

- **mean_reward**: 0.2356
- **format_ok_rate**: 0.957
- **parse_ok_rate**: 0.7892
- **q_neg_rate**: 0.3685
- **group_std_pos_rate**: 0.66
