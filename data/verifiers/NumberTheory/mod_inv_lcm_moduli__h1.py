import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        a, m1, m2 = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(a, int) or getattr(a, 'is_integer', False)
    except Exception:
        h1 = False
        
    try:
        h2 = sympy.gcd(a, m1) == 1
    except Exception:
        h2 = False
        
    try:
        h3 = sympy.gcd(a, m2) == 1
    except Exception:
        h3 = False
        
    try:
        l = sympy.lcm(m1, m2)
        q = sympy.gcd(a, l) == 1
    except Exception:
        q = False
        
    return [bool(h1), bool(h2), bool(h3), not bool(q)]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: a has a modular inverse modulo m1",
    "H_3: a has a modular inverse modulo m2",
    "¬Q: a does not have a modular inverse modulo lcm(m1, m2)"
]

N_HYP = 3
NEG_Q_INDEX = 3