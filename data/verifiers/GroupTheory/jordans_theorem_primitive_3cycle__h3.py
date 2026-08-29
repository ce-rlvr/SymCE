import math
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import eye, zeros

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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, G = witness
        else:
            G = witness
            n = getattr(G, 'degree', None)
    except Exception:
        n, G = None, None

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    try:
        h2 = isinstance(G, PermutationGroup) and G.degree == n and G.is_primitive()
    except Exception:
        h2 = False

    try:
        fact = math.factorial(int(n))
        order = G.order()
        if n == 1:
            is_An_or_Sn = (order == 1)
        else:
            is_An_or_Sn = (order == fact) or (order == fact // 2)
        neg_q = not is_An_or_Sn
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is a primitive permutation group acting on a finite set X of size n",
    "¬Q: G is neither the alternating group A_n nor the symmetric group S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2