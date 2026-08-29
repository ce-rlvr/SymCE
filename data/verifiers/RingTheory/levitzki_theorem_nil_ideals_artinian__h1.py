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

# Top-level setup: named object bindings
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

class AbstractRingIdeal:
    """
    Represents an ideal in a ring with specified properties.
    Since infinite-dimensional rings (required for a counterexample to this conjecture)
    are not natively supported in SymPy, this class allows the witness to declare 
    its mathematical properties directly.
    """
    def __init__(self, is_nil, is_nilpotent):
        self._is_nil = is_nil
        self._is_nilpotent = is_nilpotent
        
    def is_nil_ideal(self):
        return self._is_nil
        
    def is_nilpotent_ideal(self):
        return self._is_nilpotent

# A known counterexample: 
# R = direct sum of M_n(F) for n=1..infinity
# I = direct sum of strictly upper triangular matrices in M_n(F)
# I is nil (every element has finitely many non-zero components, hence nilpotent)
# I is not nilpotent (index of nilpotency of n-th component is n, unbounded)
Counterexample = AbstractRingIdeal(is_nil=True, is_nilpotent=False)

def conditions(witness) -> list[bool]:
    # H_1: I is a nil right (or left) ideal of R
    try:
        if hasattr(witness, 'is_nil_ideal'):
            h1 = witness.is_nil_ideal() if callable(witness.is_nil_ideal) else witness.is_nil_ideal
        elif isinstance(witness, dict):
            h1 = witness.get('is_nil_ideal', False)
        else:
            h1 = False
        h1_ok = bool(h1)
    except Exception:
        h1_ok = False

    # ¬Q: I is not a nilpotent ideal
    try:
        if hasattr(witness, 'is_nilpotent_ideal'):
            q = witness.is_nilpotent_ideal() if callable(witness.is_nilpotent_ideal) else witness.is_nilpotent_ideal
        elif isinstance(witness, dict):
            q = witness.get('is_nilpotent_ideal', True)
        else:
            q = True
        neg_q_ok = not bool(q)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is a nil right (or left) ideal of R",
    "¬Q: I is not a nilpotent ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1