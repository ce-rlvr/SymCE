# SFT run - 20260706-221950__64_full_run_dense__seed64__6e33172

## Configuration

- **config_yaml**: configs/seeds/64_full_run_dense.yaml
- **seed**: 64
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 1.049312210083008
- **final_eval_loss**: 0.6858243346214294

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.972
- **witness_parse_ok_rate**: 0.792
- **oracle_pass_at_1**: 0.26
- **advisory_gate_passed**: True
