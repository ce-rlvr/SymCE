import sympy as sp
from sympy import gcd, eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    h1 = h2 = h3 = h4 = neg_q = False
    try:
        if isinstance(witness, dict):
            if 'h1' in witness:
                h1 = bool(witness.get('h1', False))
                h2 = bool(witness.get('h2', False))
                h3 = bool(witness.get('h3', False))
                h4 = bool(witness.get('h4', False))
                neg_q = bool(witness.get('neg_q', False))
                return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass
        
    try:
        if hasattr(witness, 'is_integral_domain'):
            h1 = bool(witness.is_integral_domain())
            h2 = bool(witness.is_polynomial())
            h3 = bool(witness.is_invertible_fractional_ideal())
            h4 = bool(witness.is_positive_integer())
            neg_q = bool(witness.conclusion_fails())
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: f is a polynomial over R",
    "H_3: c(f) is an invertible fractional ideal",
    "H_4: n is a positive integer",
    "¬Q: c(f^n) != c(f)^n"
]

N_HYP = 4
NEG_Q_INDEX = 4