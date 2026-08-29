# RLVR run - 20260624-193329__19_full_run_dense__seed19__6e33172

## Configuration

- **config_yaml**: configs/seeds/19_full_run_dense.yaml
- **seed**: 19
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260624-185824__19_full_run_dense__seed19__6e33172/lora
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

- **final_loss**: 0.019086310267448427
- **final_reward_mean**: 0.4148310875106189
- **final_kl**: 0.29221943439915776

## Rollouts

- **mean_reward**: 0.2765
- **format_ok_rate**: 0.9778
- **parse_ok_rate**: 0.8091
- **q_neg_rate**: 0.3942
- **group_std_pos_rate**: 0.6251
