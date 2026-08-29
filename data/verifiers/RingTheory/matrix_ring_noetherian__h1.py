import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
class CustomRing:
    def __init__(self, name, noetherian=True):
        self.name = name
        self.is_left_Noetherian = noetherian
        self.is_Noetherian = noetherian

    def __str__(self):
        return self.name

# Provide standard counterexample objects for the witness to use
R_non_noeth = CustomRing("R_non_noeth", noetherian=False)
R_noeth = CustomRing("R_noeth", noetherian=True)

def conditions(witness) -> list[bool]:
    n = None
    R = None
    
    # Extract n and R from the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int):
                n, R = witness
            elif isinstance(witness[1], int):
                R, n = witness
            else:
                R, n = witness
        elif isinstance(witness, dict):
            n = witness.get('n')
            R = witness.get('R')
        elif hasattr(witness, 'n') and hasattr(witness, 'R'):
            n = witness.n
            R = witness.R
        else:
            if isinstance(witness, int):
                n = witness
                R = R_non_noeth
            else:
                R = witness
                n = 1
    except Exception:
        pass

    # H_1: n is a positive integer
    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False

    # neg_Q: M_n(R) is not a left Noetherian ring
    # M_n(R) is left Noetherian iff R is left Noetherian.
    try:
        if isinstance(R, str):
            s = R.lower()
            if "non" in s or "not" in s:
                q_holds = False
            elif "infinit" in s or "..." in s:
                q_holds = False
            else:
                q_holds = True
        elif hasattr(R, 'is_left_Noetherian'):
            q_holds = bool(R.is_left_Noetherian)
        elif hasattr(R, 'is_Noetherian'):
            q_holds = bool(R.is_Noetherian)
        elif hasattr(R, 'is_noetherian'):
            q_holds = bool(R.is_noetherian)
        else:
            # Default to True for standard SymPy domains or unknown objects
            q_holds = True
            
        neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: M_n(R) is not a left Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1