# RLVR run - 20260708-124206__64_full_run_sparse__seed64__6e33172

## Configuration

- **config_yaml**: configs/seeds/64_full_run_sparse.yaml
- **seed**: 64
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260708-120646__64_full_run_sparse__seed64__6e33172/lora
- **train_jsonl**: data/rlvr_prompts_v2.jsonl
- **reward_mode**: oracle
- **task_mode**: counterexample_only
- **oracle_reward_weights**:
    - `alpha`: 0
    - `beta`: 1
    - `gamma`: 0
    - `delta`: 0
    - `epsilon`: 1
- **num_generations**: 4
- **beta**: 0.02

## Training

- **final_loss**: 0.049335134029388425
- **final_reward_mean**: 0.3033854166666667
- **final_kl**: 0.3508365685378926

## Rollouts

- **mean_reward**: 0.1771
- **format_ok_rate**: 0.9607
- **parse_ok_rate**: 0.8101
- **q_neg_rate**: 0.3669
- **group_std_pos_rate**: 0.5789
