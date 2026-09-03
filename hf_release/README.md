# Publishing SymCE on Hugging Face

Two builders, one dataset repository and twelve model repositories. Both write
into `hf_release/build/`, which is not tracked; nothing here modifies the corpus.

```
hf_release/
  build_dataset.py       -> build/SymCE/          (one dataset repo)
  build_model_repos.py   -> build/models/<name>/  (twelve model repos + upload.sh)
```

---

## 0. One-time setup

Install the CLI and log in. The CLI is called `hf`; `huggingface-cli` is the old
name for the same tool.

```bash
pip install -U "huggingface_hub[cli]"
hf auth login          # paste a token with *write* scope
```

Create the token at <https://huggingface.co/settings/tokens>. Pick **Write**, or
a fine-grained token with write access to the `ce-rlvr` namespace.

### Create the organisation

Yes, Hugging Face has organisations, and they work like GitHub's. Free, and a
user can belong to many.

1. Go to <https://hf.co/organizations/new>.
2. Take the name `ce-rlvr` so the Hub namespace matches the GitHub org. Check it
   is free first: <https://huggingface.co/ce-rlvr> should 404.
3. Type: **Academic / Research**. Leave it public.
4. Settings -> **Members** -> invite the other four authors. Give at least one
   co-author the **admin** role so the artifacts outlive one account.
5. Settings -> **Account**: add the org avatar and a one-line description. It
   shows on every model and dataset card.

Everything below assumes the namespace is `ce-rlvr`. If you pick another name,
pass `--org <name>` to `build_model_repos.py` and edit `DATASET_REPO` at the top
of both builders, `docs/index.html`, and the `Data:` link in the
generated cards.

---

## 1. The dataset

```bash
python tools/normalise_verifier_paths.py --check    # must exit 0
python hf_release/build_dataset.py
hf repos create ce-rlvr/SymCE --repo-type dataset
hf upload ce-rlvr/SymCE hf_release/build/SymCE . --repo-type dataset
```

`build_dataset.py` refuses to run if any verifier path in the corpus is still an
absolute path from the build machine, because such a corpus cannot be executed by
anyone else.

The build is about 75 MB: seven JSONL configs, the human-audit annotations, a
`verifiers.tar.gz` of all 12,376 modules, and a `MANIFEST.sha256.json`. Every
count in the card is measured from the files being shipped.

Check it loads before you trust it:

```bash
python -c "
from datasets import load_dataset
d = load_dataset('ce-rlvr/SymCE', 'test')['test']
print(len(d), d.column_names[:5])"
```

---

## 2. The models

Twelve LoRA adapters: seeds 42, 19, 31, 64 x {SFT, RLVR-dense, RLVR-sparse}.
**Run this on the training machine**, where `runs/sft/*/lora` and
`runs/rlvr/*/lora` still exist. Adapters are small, so all twelve together are a
few hundred MB.

```bash
python hf_release/build_model_repos.py --runs-root runs
bash hf_release/build/models/upload.sh
```

The builder discovers runs from each `runs/rlvr/*/config.json`: the arm comes
from the reward weights the run actually recorded, and the SFT parent from that
run's `sft_checkpoint`. It refuses to invent a run that does not exist, and warns
loudly for any adapter directory it cannot find.

To review or edit the cards away from the GPU:

```bash
python hf_release/build_model_repos.py --cards-only
```

If `upload.sh` fails because a repository does not exist yet, `hf upload` creates
it automatically; the explicit `hf repos create` step is only needed when you
want the repo private first.

### Naming

```
ce-rlvr/symce-qwen3-4b-sft-seed42
ce-rlvr/symce-qwen3-4b-rlvr-dense-seed42
ce-rlvr/symce-qwen3-4b-rlvr-sparse-seed42
...            (and the same three for seeds 19, 31 and 64)
```

The three SFT adapters are negative results. Their cards open with a warning
banner saying so, because a checkpoint that asserts 70 % of true theorems are
false should not be downloaded by accident.

### Not published

The Gemma-3-4B adapters. Only the Qwen3-4B checkpoints are on the Hub. The
seed-24 Gemma evaluation outputs are in `runs/eval/`, so the collapse reported
for that seed is reproducible; the seed-56 outputs are not, which the repository
README states.

---

## 3. After uploading

- Add the arXiv id to the `tags:` block of every card as `arxiv:XXXX.XXXXX`. The
  Hub then links each repo to its paper page automatically. Skip it until the
  preprint exists; the tag is a no-op otherwise.
- Cross-link: the dataset card already points at the code and the models; check
  that the model cards' `datasets: [ce-rlvr/SymCE]` resolves.
- Turn on the dataset viewer (it is on by default for public repos) and confirm
  all seven configs render.
- Check the Hub links in the repository README and in `docs/index.html`, both
  of which assume the `ce-rlvr` namespace.
