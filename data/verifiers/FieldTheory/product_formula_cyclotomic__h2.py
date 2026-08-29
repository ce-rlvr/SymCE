import sympy
from sympy import Symbol, expand, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import divisors
from sympy.polys import cyclotomic_poly
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
    # H_1: n >= 1 is an integer
    try:
        if (type(witness) is int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            h1 = int(witness) >= 1
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: x^n - 1 != \prod_{d|n} \Phi_d(x)
    try:
        n = int(witness)
        x = Symbol('x')
        lhs = x**n - 1
        
        rhs = 1
        for d in divisors(n):
            rhs *= cyclotomic_poly(d, x)
            
        diff = expand(lhs - rhs)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "¬Q: x^n - 1 != \\prod_{d|n} \\Phi_d(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1