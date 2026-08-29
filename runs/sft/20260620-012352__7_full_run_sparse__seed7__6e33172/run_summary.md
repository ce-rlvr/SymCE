# SFT run - 20260620-012352__7_full_run_sparse__seed7__6e33172

## Configuration

- **config_yaml**: configs/seeds/7_full_run_sparse.yaml
- **seed**: 7
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 1.061327838897705
- **final_eval_loss**: 0.5670207738876343

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.984
- **witness_parse_ok_rate**: 0.784
- **oracle_pass_at_1**: 0.26
- **advisory_gate_passed**: True
