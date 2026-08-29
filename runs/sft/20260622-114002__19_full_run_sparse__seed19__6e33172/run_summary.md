# SFT run - 20260622-114002__19_full_run_sparse__seed19__6e33172

## Configuration

- **config_yaml**: configs/seeds/19_full_run_sparse.yaml
- **seed**: 19
- **train_jsonl**: data/sft_data_v2.jsonl
- **task_mode**: counterexample_only
- **lora_r**: 16
- **num_train_epochs**: 2.0
- **report_to**: wandb

## Training

- **final_loss**: 1.0580866813659668
- **final_eval_loss**: 0.576618492603302

## Held-out probe

- **n_prompts**: 50
- **k_samples**: 5
- **tag_parse_rate**: 0.98
- **witness_parse_ok_rate**: 0.78
- **oracle_pass_at_1**: 0.3
- **advisory_gate_passed**: True
