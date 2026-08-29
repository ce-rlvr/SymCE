# SFT run — 20260714-042109__sft_full_finetune__seed19__d84821f

## Configuration

- **config_yaml**: configs/sft_full_finetune.yaml
- **seed**: 19
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 64
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 1.5028687477111817
- **final_eval_loss**: 0.9167381525039673

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.932
- **witness_parse_ok_rate**: 0.784
- **oracle_pass_at_1**: 0.28
- **advisory_gate_passed**: True
