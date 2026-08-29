import sympy
import sympy.abc
import math
import itertools
import functools

# Top-level setup
class MockRing:
    def __init__(self, name, is_commutative=True, has_identity=True, is_noetherian=True):
        self.name = name
        self.is_commutative = is_commutative
        self.has_identity = has_identity
        self.is_noetherian = is_noetherian

    def __str__(self):
        return self.name

class MockIdeal:
    def __init__(self, ring, name, is_zero=False, quotient_is_noetherian=True):
        self.ring = ring
        self.name = name
        self.is_zero = is_zero
        self.quotient_is_noetherian = quotient_is_noetherian

    def __str__(self):
        return self.name

# Predefined objects for the witness to use
PolyInf = MockRing("k[x_1, x_2, ...]", is_commutative=True, has_identity=True, is_noetherian=False)
ZeroIdeal_PolyInf = MockIdeal(PolyInf, "{0}", is_zero=True, quotient_is_noetherian=False)

Z = MockRing("Z", is_commutative=True, has_identity=True, is_noetherian=True)
ZeroIdeal_Z = MockIdeal(Z, "{0}", is_zero=True, quotient_is_noetherian=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        if hasattr(R, 'is_commutative') and hasattr(R, 'has_identity'):
            h1 = (getattr(R, 'is_commutative') is not False) and (getattr(R, 'has_identity') is not False)
        elif hasattr(R, 'is_commutative'):
            h1 = getattr(R, 'is_commutative') is not False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    try:
        if hasattr(I, 'ring'):
            h2 = (getattr(I, 'ring') == R)
        else:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: R/I is NOT a Noetherian ring
    try:
        if hasattr(I, 'quotient_is_noetherian'):
            neg_q = not bool(getattr(I, 'quotient_is_noetherian'))
        else:
            R_str = str(R).lower().replace(" ", "")
            I_str = str(I).lower().replace(" ", "")
            
            is_non_noeth = False
            if hasattr(R, 'is_noetherian'):
                if getattr(R, 'is_noetherian') is False:
                    is_non_noeth = True
            if any(sub in R_str for sub in ["...", "dots", "inf", "c(r)", "c[0,1]", "continuous", "x_i:i"]):
                is_non_noeth = True
                
            is_zero_ideal = False
            if hasattr(I, 'is_zero'):
                if getattr(I, 'is_zero') is True:
                    is_zero_ideal = True
            if I_str in ["{0}", "0", "(0)", "ideal(0)", "zeroideal", "thezeroideal", "zero", "set([0])", "[]", "()"]:
                is_zero_ideal = True
            elif "zero" in I_str and "non" not in I_str:
                is_zero_ideal = True
                
            if is_non_noeth and is_zero_ideal:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R",
    "¬Q: The quotient ring R/I is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2