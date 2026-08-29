# SFT run — 20260513-220136__full_run__seed42__da490c1

## Configuration

- **config_yaml**: configs/full_run.yaml
- **seed**: 42
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 0.5424027252197265
- **final_eval_loss**: 0.5459294319152832

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 8
- **tag_parse_rate**: 0.995
- **witness_parse_ok_rate**: 0.6275
- **oracle_pass_at_1**: 0.14
- **advisory_gate_passed**: True
