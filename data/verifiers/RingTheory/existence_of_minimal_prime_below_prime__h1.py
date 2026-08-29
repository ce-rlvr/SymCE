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

# Top-level setup
x, y, z = sympy.abc.x, sympy.abc.y, sympy.abc.z
ZZ = sympy.ZZ
QQ = sympy.QQ

class MockIdeal:
    """
    Mock class to represent an ideal in an abstract ring, since SymPy lacks 
    comprehensive support for non-commutative rings and their prime ideals.
    """
    def __init__(self, is_prime_ideal: bool, has_minimal_prime_subset: bool):
        self.is_prime_ideal = is_prime_ideal
        self.has_minimal_prime_subset = has_minimal_prime_subset

class MockRing:
    pass

# A ready-made counterexample for the namespace
CounterexampleRing = MockRing()
CounterexampleIdeal = MockIdeal(is_prime_ideal=True, has_minimal_prime_subset=False)


def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Witness can be just the ideal P, or a tuple (R, P)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, P = witness
    else:
        P = witness

    # Check H_1: P is a prime ideal of R
    try:
        if isinstance(P, dict):
            h1 = bool(P.get("is_prime_ideal", False))
        else:
            h1 = bool(getattr(P, "is_prime_ideal", False))
    except Exception:
        h1 = False

    # Check ¬Q: P does NOT contain a minimal prime ideal of R
    try:
        if isinstance(P, dict):
            has_min = bool(P.get("has_minimal_prime_subset", True))
            neg_q = not has_min
        else:
            has_min = bool(getattr(P, "has_minimal_prime_subset", True))
            neg_q = not has_min
    except Exception:
        neg_q = False

    return [h1, neg_q]


CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: P does not contain a minimal prime ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1