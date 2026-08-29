# RLVR run - 20260620-020121__7_full_run_sparse__seed7__6e33172

## Configuration

- **config_yaml**: configs/seeds/7_full_run_sparse.yaml
- **seed**: 7
- **sft_checkpoint**: /home/omar-farouk-zouak/Projects/pfe/rlvr-find-counterexample/runs/sft/20260620-012352__7_full_run_sparse__seed7__6e33172/lora
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

- **final_loss**: 0.017542779445648193
- **final_reward_mean**: 0.3055555555555556
- **final_kl**: 0.5523186610339003

## Rollouts

- **mean_reward**: 0.1725
- **format_ok_rate**: 0.9615
- **parse_ok_rate**: 0.808
- **q_neg_rate**: 0.3645
- **group_std_pos_rate**: 0.568
