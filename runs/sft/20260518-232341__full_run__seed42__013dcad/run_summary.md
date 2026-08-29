# SFT run — 20260518-232341__full_run__seed42__013dcad

## Configuration

- **config_yaml**: configs/full_run.yaml
- **seed**: 42
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 4.0
- **report_to**: wandb

## Training

- **final_loss**: 1.0446589469909668
- **final_eval_loss**: 0.5800058841705322

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 8
- **tag_parse_rate**: 0.99
- **witness_parse_ok_rate**: 0.7775
- **oracle_pass_at_1**: 0.16
- **advisory_gate_passed**: True
