import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

class Ring:
    """
    A simple class to represent a mathematical ring for the purpose of this verifier.
    """
    def __init__(self, is_commutative=True, is_local=False, intersection_zero=True):
        self.is_commutative = is_commutative
        self.is_local = is_local
        self.intersection_zero = intersection_zero

# Standard algebra objects
Z = Ring(is_commutative=True, is_local=False, intersection_zero=True)
Q = Ring(is_commutative=True, is_local=True, intersection_zero=True)

# Known counterexamples to the Krull Intersection Theorem without the Noetherian hypothesis
C_infty_germs = Ring(is_commutative=True, is_local=True, intersection_zero=False)
ValuationRingHeight2 = Ring(is_commutative=True, is_local=True, intersection_zero=False)

def conditions(witness):
    # H1: R is a commutative ring
    h1 = False
    try:
        if hasattr(witness, 'is_commutative'):
            h1 = bool(witness.is_commutative)
        elif isinstance(witness, str):
            h1 = "non-commutative" not in witness.lower()
    except Exception:
        pass

    # H2: R is a local ring with maximal ideal m
    h2 = False
    try:
        if hasattr(witness, 'is_local'):
            h2 = bool(witness.is_local)
        elif isinstance(witness, str):
            h2 = "local" in witness.lower() or "germ" in witness.lower() or "valuation" in witness.lower()
    except Exception:
        pass

    # ¬Q: The intersection of m^n for all positive integers n is NOT the zero ideal
    neg_q = False
    try:
        if hasattr(witness, 'intersection_zero'):
            neg_q = not bool(witness.intersection_zero)
        elif isinstance(witness, str):
            neg_q = "germ" in witness.lower() or "valuation" in witness.lower() or "non-noetherian" in witness.lower()
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m",
    "¬Q: The intersection of m^n for all positive integers n is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2