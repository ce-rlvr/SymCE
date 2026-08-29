# SFT run - 20260624-185824__19_full_run_dense__seed19__6e33172

## Configuration

- **config_yaml**: configs/seeds/19_full_run_dense.yaml
- **seed**: 19
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 1.0583857536315917
- **final_eval_loss**: 0.5761923789978027

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.984
- **witness_parse_ok_rate**: 0.732
- **oracle_pass_at_1**: 0.24
- **advisory_gate_passed**: True
