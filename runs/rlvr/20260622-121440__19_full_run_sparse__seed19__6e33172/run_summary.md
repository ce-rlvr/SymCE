# RLVR run - 20260622-121440__19_full_run_sparse__seed19__6e33172

## Configuration

- **config_yaml**: configs/seeds/19_full_run_sparse.yaml
- **seed**: 19
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260622-114002__19_full_run_sparse__seed19__6e33172/lora
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

- **final_loss**: 0.04216448068618774
- **final_reward_mean**: 0.3059895833333333
- **final_kl**: 0.1993897273334571

## Rollouts

- **mean_reward**: 0.1711
- **format_ok_rate**: 0.9691
- **parse_ok_rate**: 0.8134
- **q_neg_rate**: 0.3576
- **group_std_pos_rate**: 0.558
