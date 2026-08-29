import sympy
from sympy import symbols
import math
import itertools
import functools

class RingTheoryWitness:
    """
    Helper class for constructing a witness in the module's namespace.
    A witness can be an instance of this class or a dictionary with matching keys.
    """
    def __init__(self, I_is_proper, I_has_primary_decomp, P_is_prime, P_contains_I, P_contains_min_assoc_prime):
        self.I_is_proper = bool(I_is_proper)
        self.I_has_primary_decomp = bool(I_has_primary_decomp)
        self.P_is_prime = bool(P_is_prime)
        self.P_contains_I = bool(P_contains_I)
        self.P_contains_min_assoc_prime = bool(P_contains_min_assoc_prime)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('I_is_proper', False) and witness.get('I_has_primary_decomp', False))
        else:
            h1 = bool(witness.I_is_proper and witness.I_has_primary_decomp)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('P_is_prime', False) and witness.get('P_contains_I', False))
        else:
            h2 = bool(witness.P_is_prime and witness.P_contains_I)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            q = bool(witness.get('P_contains_min_assoc_prime', True))
        else:
            q = bool(witness.P_contains_min_assoc_prime)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R that admits a primary decomposition",
    "H_2: P is a prime ideal of R containing I",
    "¬Q: P does not contain any minimal associated prime ideal of I"
]

N_HYP = 2
NEG_Q_INDEX = 2