import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup
# (No specific named bindings needed for this abstract property check, 
# as SymPy does not natively support non-Noetherian rings or Ass(M).
# The witness is expected to be a dictionary or object mocking the module's properties.)

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "¬Q: The equivalence fails (M does not have finite length, but every prime ideal in Ass(M) is maximal)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            is_fg = bool(witness.get("is_finitely_generated", witness.get("is_fg", False)))
            fin_len = bool(witness.get("has_finite_length", witness.get("fin_len", False)))
            ass_max = bool(witness.get("ass_primes_are_maximal", witness.get("ass_max", False)))
        else:
            is_fg = bool(getattr(witness, "is_finitely_generated", getattr(witness, "is_fg", False)))
            fin_len = bool(getattr(witness, "has_finite_length", getattr(witness, "fin_len", False)))
            ass_max = bool(getattr(witness, "ass_primes_are_maximal", getattr(witness, "ass_max", False)))

        # Mathematical constraint: If M has finite length, it has a composition series 
        # of simple modules. The annihilators of these simple modules are maximal ideals.
        # Ass(M) is a subset of these maximal ideals. 
        # Therefore, finite length ALWAYS implies every prime in Ass(M) is maximal, over ANY ring.
        # A valid counterexample to the equivalence must have fin_len == False and ass_max == True.
        if fin_len and not ass_max:
            return [False, False]

        h1 = is_fg
        
        # The conjecture claims: fin_len <=> ass_max
        # The conclusion fails if the two truth values are different.
        neg_q = (fin_len != ass_max)

        return [h1, neg_q]
    except Exception:
        return [False, False]