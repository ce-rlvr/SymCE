# SFT run — 20260517-215205__full_run__seed42__d5c4485

## Configuration

- **config_yaml**: configs/full_run.yaml
- **seed**: 42
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 3.0
- **report_to**: wandb

## Training

- **final_loss**: 0.7952018737792969
- **final_eval_loss**: 0.5486702919006348

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 8
- **tag_parse_rate**: 0.9875
- **witness_parse_ok_rate**: 0.7125
- **oracle_pass_at_1**: 0.12
- **advisory_gate_passed**: True
