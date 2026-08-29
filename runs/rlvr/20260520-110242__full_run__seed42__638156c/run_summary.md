# RLVR run - 20260520-110242__full_run__seed42__638156c

## Configuration

- **config_yaml**: configs/full_run.yaml
- **seed**: 42
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260520-060436__full_run__seed42__638156c/lora
- **train_jsonl**: data/rlvr_prompts_v2.jsonl
- **reward_mode**: oracle
- **task_mode**: counterexample_only
- **oracle_reward_weights**:
    - `alpha`: 0.25
    - `beta`: 0.75
    - `gamma`: 0.1
    - `delta`: 0.25
    - `epsilon`: 1.0
- **num_generations**: 4
- **beta**: 0.02

## Training

- **final_loss**: 0.012989328801631927
- **final_reward_mean**: 0.4722692567544679
- **final_kl**: 0.43917294521816075

## Rollouts

- **mean_reward**: 0.2991
- **format_ok_rate**: 0.9767
- **parse_ok_rate**: 0.7985
- **q_neg_rate**: 0.3878
- **group_std_pos_rate**: 0.6497
