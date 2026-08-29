# SFT run — 20260523-225145__full_run_dense_better__seed42__2afa2a7

## Configuration

- **config_yaml**: configs/full_run_dense_better.yaml
- **seed**: 42
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 1.0453617095947265
- **final_eval_loss**: 0.5855732560157776

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.984
- **witness_parse_ok_rate**: 0.748
- **oracle_pass_at_1**: 0.32
- **advisory_gate_passed**: True
