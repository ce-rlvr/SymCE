import sympy
import math
import itertools
import functools

# Top-level setup for witness evaluation
# (No special named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Ensure the witness is an integer
        if int(witness) != witness or isinstance(witness, bool):
            return [False, False]
        p = int(witness)
    except Exception:
        return [False, False]

    # H_1: p > 3
    try:
        h1 = p > 3
    except Exception:
        h1 = False

    # ¬Q: The sum of the quadratic residues modulo p in {1, ..., p-1} is not congruent to 0 modulo p
    try:
        if p <= 0:
            neg_q = False
        else:
            # Find all unique non-zero squares modulo p
            residues = set((x**2) % p for x in range(p))
            residues.discard(0)
            
            sum_residues = sum(residues)
            neg_q = (sum_residues % p != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p > 3",
    "¬Q: The sum of the quadratic residues modulo p in {1, ..., p-1} is not congruent to 0 modulo p"
]

N_HYP = 1
NEG_Q_INDEX = 1