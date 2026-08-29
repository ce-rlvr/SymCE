import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.abc
from sympy.polys import domains
import z3
import math
import itertools
import functools

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
    try:
        h1 = witness.is_integral_domain()
    except Exception:
        try:
            h1 = all(witness.mul(x, y) != witness.zero for x in witness.elements if x != witness.zero for y in witness.elements if y != witness.zero)
        except Exception:
            h1 = False

    try:
        neg_q = witness.neg_q()
    except Exception:
        try:
            E, M, O, a, b = witness.elements, witness.mul, witness.one, witness.a, witness.b
            U = {u for u in E if any(M(u, v) == O for v in E)}
            assoc = any(a == M(u, b) for u in U)
            ideal_eq = any(a == M(x, b) for x in E) and any(b == M(y, a) for y in E)
            neg_q = (assoc != ideal_eq)
        except Exception:
            neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: a and b are associates iff (a) = (b) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1