# RLVR run - 20260618-025136__7_full_run_dense__seed7__6e33172

## Configuration

- **config_yaml**: configs/seeds/7_full_run_dense.yaml
- **seed**: 7
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260618-021434__7_full_run_dense__seed7__6e33172/lora
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

- **final_loss**: 0.030561575293540956
- **final_reward_mean**: 0.37530020096649724
- **final_kl**: 0.23360262998741949

## Rollouts

- **mean_reward**: 0.2634
- **format_ok_rate**: 0.9707
- **parse_ok_rate**: 0.7991
- **q_neg_rate**: 0.3959
- **group_std_pos_rate**: 0.6378
