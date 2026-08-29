# SFT run — 20260518-195751__full_run__seed42__d5c4485

## Configuration

- **config_yaml**: configs/full_run.yaml
- **seed**: 42
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 5.0
- **report_to**: wandb

## Training

- **final_loss**: 1.0404696464538574
- **final_eval_loss**: 0.763761579990387

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 8
- **tag_parse_rate**: 0.885
- **witness_parse_ok_rate**: 0.48
- **oracle_pass_at_1**: 0.1
- **advisory_gate_passed**: True
