"""
Hypothesis-dropping mutation for algebraic theorems.

Given a true theorem: ∀x. (H₁ ∧ H₂ ∧ ... ∧ Hₙ) → Q
We drop one droppable hypothesis Hᵢ to obtain the FALSE conjecture:
    ∀x. (H₁ ∧ ... ∧ H_{i-1} ∧ H_{i+1} ∧ ... ∧ Hₙ) → Q

The counterexample task is to find:
    ∃x. (remaining hypotheses hold at x) ∧ (¬Q at x)

CRITICAL: The witness x must satisfy the remaining hypotheses AND falsify
the conclusion. Finding x where Q(x) is True would be existential
satisfiability — the wrong task.
"""

from typing import Optional


def get_droppable_hypotheses(theorem: dict) -> list[dict]:
    """Return all hypotheses marked as droppable."""
    return [h for h in theorem.get("hypotheses", []) if h.get("droppable", False)]


def mutate_theorem(theorem: dict, drop_index: int = 0) -> Optional[dict]:
    """
    Create a mutation dict by dropping the drop_index-th droppable hypothesis.

    Returns None if the theorem has no droppable hypotheses.
    """
    droppable = get_droppable_hypotheses(theorem)
    if not droppable:
        return None
    drop_index = min(drop_index, len(droppable) - 1)

    dropped_hyp = droppable[drop_index]
    remaining_hyps = [h for h in theorem["hypotheses"] if h["id"] != dropped_hyp["id"]]

    remaining_texts = [h["text"] for h in remaining_hyps]
    remaining_bulleted = "\n  - ".join(remaining_texts)

    # Clean conjecture: no dropped-hypothesis metadata. This is what the trained
    # model sees during RLVR and evaluation — exposing the dropped hypothesis
    # name would allow the model to trivially target the missing condition.
    false_conjecture = (
        f"Claim: For all mathematical objects satisfying:\n"
        f"  - {remaining_bulleted}\n"
        f"the following conclusion holds:\n"
        f"  {theorem['conclusion']}"
    )

    # Annotated version kept for internal bookkeeping and debugging ONLY.
    # NEVER include this in training prompts or evaluation inputs.
    false_conjecture_annotated = (
        f"[FALSE CONJECTURE — dropped hypothesis: '{dropped_hyp['name']}']\n"
        + false_conjecture
    )

    return {
        "theorem_id": theorem["id"],
        "theorem_name": theorem["name"],
        "domain": theorem.get("domain", "Algebra"),
        "dropped_hypothesis": dropped_hyp,
        "remaining_hypotheses": remaining_hyps,
        "conclusion": theorem["conclusion"],
        "false_conjecture": false_conjecture,
        "false_conjecture_annotated": false_conjecture_annotated,
        "original_full_statement": theorem["full_statement"],
    }


def build_prompt(mutation: dict) -> str:
    """
    Build the user-turn prompt for the LLM generator.

    The system prompt lives in generator_llm.py. This function produces the
    per-theorem user message that encodes the specific mutation.
    """
    remaining_hyps = mutation["remaining_hypotheses"]
    dropped_hyp = mutation["dropped_hypothesis"]
    conclusion = mutation["conclusion"]

    remaining_numbered = "\n".join(
        f"  [{i + 1}] {h['text']}" for i, h in enumerate(remaining_hyps)
    )

    prompt = f"""## Mathematical Task: Find a Counterexample in Abstract Algebra

### Domain
{mutation['domain']}

### Original TRUE Theorem (all hypotheses present)
{mutation['original_full_statement']}

### Mutation: Dropped Hypothesis
The following hypothesis has been REMOVED, making the conjecture FALSE:
  **Dropped:** {dropped_hyp['text']}

### Remaining Hypotheses (your counterexample MUST satisfy ALL of these)
{remaining_numbered}

### Conclusion (this must FAIL at your counterexample)
  {conclusion}

---

### Your Logical Task

Find a concrete mathematical object `x` (or a tuple of objects) such that:

  ✓ ALL remaining hypotheses hold at x — verify with:
    `assert <remaining_hypothesis_check>` for each one

  ✗ The conclusion is FALSE at x — verify with:
    `assert not <conclusion_check>`
    (or equivalently: `assert <lhs> != <rhs>` for an equality conclusion)

### MANDATORY CORRECTNESS CHECK

The bug to avoid: asserting that the conclusion is TRUE.
  - WRONG:  `assert conclusion_holds(x)`      # existential satisfiability
  - CORRECT: `assert not conclusion_holds(x)` # negation — actual disproof

Every counterexample script MUST contain at least one negation-form assertion.

### Output Format
Output ONLY valid Python code. No prose, no markdown, no explanations.
Begin directly with import statements.
"""
    return prompt
