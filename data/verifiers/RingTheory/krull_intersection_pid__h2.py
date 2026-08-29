import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z

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
    "H_1: R is a principal ideal domain",
    "H_2: I is a proper ideal of R",
    "¬Q: The intersection of I^n is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    res = [False, False, False]
    try:
        n, a = map(int, witness)
    except Exception:
        return res
        
    try:
        res[0] = bool(n > 1)
    except Exception:
        pass
        
    try:
        res[1] = bool(math.gcd(a, n) > 1 and a % n != 0)
    except Exception:
        pass
        
    try:
        res[2] = bool(pow(a, n, n) != 0)
    except Exception:
        pass
        
    return res