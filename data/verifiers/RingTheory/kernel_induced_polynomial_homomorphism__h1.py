import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('h1', False))
            h2 = bool(witness.get('h2', False))
            neg_q = bool(witness.get('neg_q', False))
        else:
            h1 = bool(getattr(witness, 'h1', False))
            h2 = bool(getattr(witness, 'h2', False))
            neg_q = bool(getattr(witness, 'neg_q', False))
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: F is the induced ring homomorphism from the polynomial ring over R to the polynomial ring over S",
    "¬Q: The kernel of F is not the ideal of polynomials whose coefficients all belong to the kernel of f"
]

N_HYP = 2
NEG_Q_INDEX = 2