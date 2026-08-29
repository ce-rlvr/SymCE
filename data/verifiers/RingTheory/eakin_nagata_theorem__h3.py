import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

class Ring:
    """
    Mock object to represent abstract rings since SymPy does not natively 
    support rings with infinitely many variables or non-Noetherian properties.
    """
    def __init__(self, name, is_commutative, is_noetherian):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian

    def __repr__(self):
        return self.name

# Standard rings
Z = Ring("Z", True, True)
Q = Ring("Q", True, True)
Q_x = Ring("Q[x]", True, True)

# Counterexample 1: Polynomial ring in infinitely many variables and its fraction field
Q_poly_inf = Ring("Q[x1, x2, ...]", True, False)
Q_frac_inf = Ring("Q(x1, x2, ...)", True, True)

# Counterexample 2: Z + xQ[x] and Q[x]
Z_plus_xQx = Ring("Z + xQ[x]", True, False)

_subrings = {
    (Z, Q),
    (Z, Z),
    (Q, Q),
    (Q_x, Q_x),
    (Q_poly_inf, Q_frac_inf),
    (Q_poly_inf, Q_poly_inf),
    (Q_frac_inf, Q_frac_inf),
    (Z_plus_xQx, Q_x),
    (Z_plus_xQx, Z_plus_xQx)
}

def is_subring(R, S):
    if (R, S) in _subrings:
        return True
    # Allow duck-typing if the user created a custom relation
    if hasattr(R, 'is_subring_of'):
        try:
            return R.is_subring_of(S)
        except Exception:
            pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, S) representing the two rings.
    """
    try:
        R, S = witness
    except Exception:
        return [False, False, False]

    # H_1: R and S are commutative rings such that R is a subring of S
    try:
        h1 = bool(getattr(R, 'is_commutative', False) and 
                  getattr(S, 'is_commutative', False) and 
                  is_subring(R, S))
    except Exception:
        h1 = False

    # H_2: S is a Noetherian ring
    try:
        h2 = bool(getattr(S, 'is_noetherian', False))
    except Exception:
        h2 = False

    # ¬Q: R is NOT a Noetherian ring
    try:
        # Default to True (Noetherian) if unknown, so it fails to be a counterexample
        neg_q = not bool(getattr(R, 'is_noetherian', True))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings such that R is a subring of S",
    "H_2: S is a Noetherian ring",
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2