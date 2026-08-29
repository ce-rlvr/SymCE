# RLVR run - 20260703-171217__31_full_run_sparse__seed31__6e33172

## Configuration

- **config_yaml**: configs/seeds/31_full_run_sparse.yaml
- **seed**: 31
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260703-163538__31_full_run_sparse__seed31__6e33172/lora
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

- **final_loss**: 0.03304716646671295
- **final_reward_mean**: 0.24696180555555555
- **final_kl**: 0.23576444251618037

## Rollouts

- **mean_reward**: 0.1623
- **format_ok_rate**: 0.9652
- **parse_ok_rate**: 0.8014
- **q_neg_rate**: 0.3608
- **group_std_pos_rate**: 0.5928
