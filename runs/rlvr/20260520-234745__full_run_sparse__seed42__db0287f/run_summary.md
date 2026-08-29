# RLVR run - 20260520-234745__full_run_sparse__seed42__db0287f

## Configuration

- **config_yaml**: configs/full_run_sparse.yaml
- **seed**: 42
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260520-060436__full_run__seed42__638156c/lora
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

- **final_loss**: 0.03743517696857453
- **final_reward_mean**: 0.2916666666666667
- **final_kl**: 0.3111756649903125

## Rollouts

- **mean_reward**: 0.1579
- **format_ok_rate**: 0.9567
- **parse_ok_rate**: 0.7936
- **q_neg_rate**: 0.3642
- **group_std_pos_rate**: 0.5957
