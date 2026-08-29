# SFT run — 20260714-153627__sft_full_finetune__seed42__d84821f

## Configuration

- **config_yaml**: configs/sft_full_finetune.yaml
- **seed**: 42
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 32
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 1.719929313659668
- **final_eval_loss**: 1.2136802673339844

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.316
- **witness_parse_ok_rate**: 0.28
- **oracle_pass_at_1**: 0.1
- **advisory_gate_passed**: False
