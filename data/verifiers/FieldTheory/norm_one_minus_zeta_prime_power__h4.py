import sympy
from sympy import I, pi, exp, simplify, isprime, Integer, Rational
from sympy import minpoly, Dummy
from sympy.ntheory import totient
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k >= 1 is an integer",
    "H_3: zeta is a primitive p^k-th root of unity",
    "¬Q: Norm of (1 - zeta) is not p"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        p, k, zeta = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: k >= 1 is an integer
    try:
        h2 = bool(isinstance(k, (int, Integer)) and k >= 1)
    except Exception:
        h2 = False
        
    # H_3: zeta is a primitive p^k-th root of unity
    try:
        if not (h1 and h2):
            h3 = False
        else:
            n = int(p**k)
            cond1 = simplify(zeta**n - 1) == 0
            cond2 = simplify(zeta**(n // int(p)) - 1) != 0
            h3 = bool(cond1 and cond2)
    except Exception:
        h3 = False
        
    # ¬Q: Norm of (1 - zeta) is not p
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            x = Dummy('x')
            poly = minpoly(1 - zeta, x)
            d = poly.degree()
            a_0 = poly.coeff(x, 0)
            norm_val = ((-1)**d) * a_0
            
            deg_extension = totient(p**k)
            power = deg_extension // d
            full_norm = norm_val ** power
            
            neg_q = bool(simplify(full_norm - p) != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]