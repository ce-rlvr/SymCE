import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import sympy.matrices
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: G is the projective general linear group PGL(n, F)",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, n, q = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(sympy.ntheory.isprimepower(q))
    except Exception:
        h1 = False
        
    try:
        if n <= 0:
            expected_order = 1
        else:
            expected_order = 1
            for i in range(n):
                expected_order *= (q**n - q**i)
            expected_order = expected_order // (q - 1)
        
        h2 = hasattr(G, "order") and G.order() == expected_order
    except Exception:
        h2 = False
        
    try:
        neg_q = hasattr(G, "center") and G.center().order() > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]