# SFT run - 20260520-060436__full_run__seed42__638156c

## Configuration

- **config_yaml**: configs/full_run.yaml
- **seed**: 42
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 3.0
- **report_to**: wandb

## Training

- **final_loss**: 0.5414661884307861
- **final_eval_loss**: 0.5309804677963257

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.996
- **witness_parse_ok_rate**: 0.74
- **oracle_pass_at_1**: 0.3
- **advisory_gate_passed**: True
