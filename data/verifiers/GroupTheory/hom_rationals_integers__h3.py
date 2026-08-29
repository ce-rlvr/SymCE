import sympy
from sympy import Rational, Integer
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a function f: Q -> Z.
    """
    test_vals = [
        Rational(0), Rational(1), Rational(-1), 
        Rational(1, 2), Rational(-1, 2), 
        Rational(2, 3), Rational(3, 4), Rational(5, 8)
    ]
    
    # H_1: Let Q be the additive group of rational numbers.
    # We interpret this as the witness being a callable that accepts rational numbers.
    try:
        res = [witness(x) for x in test_vals]
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: Let Z be the additive group of integers.
    # We interpret this as the witness returning integers for the rational inputs.
    try:
        if h1_ok:
            h2_ok = all(isinstance(y, (int, Integer)) for y in res)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: f is not the trivial homomorphism (does not map every element of Q to 0)
    try:
        if h1_ok and h2_ok:
            neg_q_ok = any(y != 0 for y in res)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let Q be the additive group of rational numbers (witness accepts rationals)",
    "H_2: Let Z be the additive group of integers (witness returns integers)",
    "¬Q: f is not the trivial homomorphism (does not map every element to 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2