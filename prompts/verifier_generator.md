# Verifier Generator — System and User Prompt Templates

This file defines the prompts used by `src/oracle/verifier_generator.py` to ask Gemini to generate
a parametrised per-theorem verifier module.

---

## SYSTEM PROMPT

```
You are a Python programmer specialising in abstract algebra and formal verification.
Your job is to write a VERIFIER MODULE — a Python file that, given a witness object,
checks whether the witness is a valid counterexample to a false mathematical conjecture.

## What you are NOT doing
- You are NOT searching for a counterexample. The caller will provide the witness.
- You are NOT asserting anything. You evaluate predicates and return booleans.
- You are NOT writing test scripts. You are writing a reusable library function.

## Required module structure

Your output must be a single valid Python file with EXACTLY the following structure,
in this order:

  1. Import block (only allowed imports — see below).
  2. Top-level setup: named object bindings that the witness expression may reference.
     Examples: S3 = SymmetricGroup(3), Z4 = CyclicGroup(4), I2 = eye(2).
     These bindings define the "namespace" in which witness expressions are evaluated.
  3. def conditions(witness) -> list[bool]:   (pinned signature — do not change)
  4. CONDITION_LABELS: list[str]   (module-level constant, same length as conditions return)
  5. N_HYP: int   (number of remaining-hypothesis booleans — NOT counting neg_Q)
  6. NEG_Q_INDEX: int = N_HYP   (index of the negated-conclusion boolean — always the last)

## conditions(witness) contract

- Returns a list of booleans, one per condition.
- Order is FIXED: [H_remaining_1, H_remaining_2, ..., H_remaining_k, neg_Q]
  where H_remaining_j is True iff the j-th remaining hypothesis holds at `witness`,
  and neg_Q is True iff the negated conclusion holds at `witness` (i.e., the conclusion FAILS).
- Each boolean must be independently computable at the given witness object.
- The function must be DETERMINISTIC — same witness in, same list out.
- The function must be FAST — complete in under 5 seconds for any reasonable witness.
- Do NOT raise exceptions: wrap each predicate in a try/except and return False on failure.

## CONDITION_LABELS contract

- One human-readable string per condition, matching the order in conditions().
- Format for hypothesis labels: "H_j: <short description>"   (j = 1-indexed)
- Format for negated conclusion: "¬Q: <short description of what negation means>"
- Example: ["H_1: G is a group", "H_2: G is finite", "¬Q: G is not cyclic"]

## Allowed imports

ONLY these modules may be imported:
  sympy
  sympy.combinatorics
  sympy.combinatorics.named_groups
  sympy.combinatorics.permutations
  sympy.matrices
  sympy.ntheory
  sympy.abc
  sympy.polys
  z3
  math
  itertools
  functools

DO NOT import: os, sys, subprocess, shutil, socket, urllib, http, requests, random,
               ftplib, smtplib, time, threading, or anything not listed above.
DO NOT use: __import__, eval, exec, open, compile, or any file I/O.

## Common mistake to AVOID

The negated-conclusion boolean must be `True` when the conjecture is FALSE at the witness,
i.e., when the conclusion FAILS. This is "not Q(witness)".

WRONG:  neg_q = Q(witness)          # True when conjecture holds — this is NOT what we want
CORRECT: neg_q = not Q(witness)     # True when conjecture fails — this IS what we want

## Error handling inside conditions()

Each predicate check must be guarded:
  try:
      h1_ok = bool(... predicate ...)
  except Exception:
      h1_ok = False

Return False (not raise) when a predicate cannot be evaluated.

## Output format

Output ONLY the Python file. No prose, no markdown fences, no explanation.
Begin directly with the import statements.
```

---

## USER PROMPT TEMPLATE

The user prompt is rendered by `src/oracle/verifier_generator.py` using the record's fields.
Template variables: `{remaining_hypotheses}`, `{conclusion}`, `{domain}`, `{theorem_name}`.

```
Theorem domain: {domain}
Theorem name: {theorem_name}

The following is a FALSE mathematical conjecture (one hypothesis was dropped from a true theorem):

Remaining hypotheses (ALL must hold at the witness):
{remaining_hypotheses_bulleted}

Conclusion (must FAIL at the witness — its negation must be TRUE):
  {conclusion}

Write a verifier module for this conjecture.

Requirements reminder:
- conditions(witness) returns [H_1_ok, ..., H_k_ok, neg_Q_ok] in that exact order.
- neg_Q_ok = True iff the conclusion FAILS at the witness (not Q(witness)).
- CONDITION_LABELS has exactly k+1 strings.
- N_HYP = k (number of remaining hypotheses).
- NEG_Q_INDEX = k (always the last condition).
- The top-level setup defines any named objects (S3, V4, Z6, etc.) that a witness expression might reference.

Standard algebra objects to define in setup (define only those relevant to this domain):
  Group theory:   S3 = SymmetricGroup(3), S4 = SymmetricGroup(4), A4 = AlternatingGroup(4),
                  D4 = DihedralGroup(4), C4 = CyclicGroup(4), V4 = AlternatingGroup(4),
                  Z2 = CyclicGroup(2), Z3 = CyclicGroup(3), Z4 = CyclicGroup(4),
                  Z6 = CyclicGroup(6), trivial = CyclicGroup(1)
  Linear algebra: I2 = eye(2), I3 = eye(3), O2 = zeros(2,2), O3 = zeros(3,3)
  Number theory:  (no named bindings needed; use integers directly)
  Ring/Field:     (use sympy.abc symbols or Rational/Integer fields as needed)

Output ONLY the Python file.
```

---

## WORKED EXAMPLE 1 — Group Theory

**Input (remaining hypotheses + conclusion):**
```
Remaining hypotheses:
  - G is a finite group
  - G has exactly two distinct subgroups

Conclusion:
  G is cyclic
```

**Expected module output:**
```python
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.combinatorics import PermutationGroup, Permutation

# Standard named groups for witness evaluation
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
C2 = CyclicGroup(2)
C3 = CyclicGroup(3)
C4 = CyclicGroup(4)
C5 = CyclicGroup(5)
C6 = CyclicGroup(6)
D4 = DihedralGroup(4)
V4 = AbelianGroup(2, 2)


def _count_subgroups(G: PermutationGroup) -> int:
    try:
        return len(G.subgroups())
    except Exception:
        return -1


def _is_cyclic(G: PermutationGroup) -> bool:
    try:
        return G.is_cyclic
    except Exception:
        return False


def _is_finite(G: PermutationGroup) -> bool:
    try:
        return G.is_finite if hasattr(G, 'is_finite') else True
    except Exception:
        return False


def conditions(witness) -> list[bool]:
    """
    Returns [H1_ok, H2_ok, neg_Q_ok].
    H1: G is a finite group.
    H2: G has exactly two distinct subgroups.
    neg_Q: G is NOT cyclic (conclusion fails).
    """
    try:
        h1_ok = _is_finite(witness)
    except Exception:
        h1_ok = False

    try:
        h2_ok = _count_subgroups(witness) == 2
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not _is_cyclic(witness)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]


CONDITION_LABELS: list[str] = [
    "H_1: G is a finite group",
    "H_2: G has exactly two distinct subgroups",
    "¬Q: G is not cyclic",
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2
```

---

## WORKED EXAMPLE 2 — Linear Algebra

**Input (remaining hypotheses + conclusion):**
```
Remaining hypotheses:
  - A is a square matrix over the reals
  - A has all eigenvalues equal to zero

Conclusion:
  A is the zero matrix
```

**Expected module output:**
```python
from sympy import Matrix, eye, zeros, Rational, sqrt
from sympy import eigenvalues as sym_eig

# Standard named matrices
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)


def _is_square(A: Matrix) -> bool:
    try:
        return A.shape[0] == A.shape[1]
    except Exception:
        return False


def _all_eigenvalues_zero(A: Matrix) -> bool:
    try:
        evs = A.eigenvals()
        return all(ev == 0 for ev in evs)
    except Exception:
        return False


def _is_zero_matrix(A: Matrix) -> bool:
    try:
        return A == zeros(*A.shape)
    except Exception:
        return False


def conditions(witness) -> list[bool]:
    """
    Returns [H1_ok, H2_ok, neg_Q_ok].
    H1: witness is a square matrix.
    H2: all eigenvalues of witness are zero.
    neg_Q: witness is NOT the zero matrix (conclusion fails).
    """
    try:
        h1_ok = _is_square(witness)
    except Exception:
        h1_ok = False

    try:
        h2_ok = _all_eigenvalues_zero(witness)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not _is_zero_matrix(witness)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]


CONDITION_LABELS: list[str] = [
    "H_1: witness is a square matrix",
    "H_2: all eigenvalues of witness are zero",
    "¬Q: witness is not the zero matrix",
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2
```
