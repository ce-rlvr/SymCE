# SFT run - 20260618-021434__7_full_run_dense__seed7__6e33172

## Configuration

- **config_yaml**: configs/seeds/7_full_run_dense.yaml
- **seed**: 7
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 1.060847282409668
- **final_eval_loss**: 0.5665738582611084

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.98
- **witness_parse_ok_rate**: 0.796
- **oracle_pass_at_1**: 0.26
- **advisory_gate_passed**: True
