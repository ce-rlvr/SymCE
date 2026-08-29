import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
# (No specific named bindings needed for this abstract property check,
# but standard imports are provided as requested)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The witness can be a dictionary, an object with attributes, or a tuple.
    Tuple formats supported:
      - (F_rank, N_rank)
      - (R_is_PID, F_is_free, F_rank, N_is_free, N_rank)
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                F_rank, N_rank = witness
                R_is_PID = True
                F_is_free = True
                N_is_free = True
            elif len(witness) == 5:
                R_is_PID, F_is_free, F_rank, N_is_free, N_rank = witness
            else:
                R_is_PID = False
                F_is_free = False
                F_rank = -1
                N_is_free = False
                N_rank = float('inf')
        elif isinstance(witness, dict):
            R_is_PID = witness.get("R_is_PID", False)
            F_is_free = witness.get("F_is_free", False)
            F_rank = witness.get("F_rank", -1)
            N_is_free = witness.get("N_is_free", False)
            N_rank = witness.get("N_rank", float('inf'))
        else:
            R_is_PID = getattr(witness, "R_is_PID", False)
            F_is_free = getattr(witness, "F_is_free", False)
            F_rank = getattr(witness, "F_rank", -1)
            N_is_free = getattr(witness, "N_is_free", False)
            N_rank = getattr(witness, "N_rank", float('inf'))
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(R_is_PID)
    except Exception:
        h1 = False

    try:
        h2 = bool(F_is_free) and isinstance(F_rank, int) and F_rank >= 0
    except Exception:
        h2 = False

    try:
        # Conclusion: N is a free R-module of rank m such that m <= n
        q = bool(N_is_free) and (N_rank is not None) and (N_rank <= F_rank)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: F is a free R-module of finite rank n",
    "¬Q: N is not a free R-module of rank m such that m <= n"
]

N_HYP = 2
NEG_Q_INDEX = 2