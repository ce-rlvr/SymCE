import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            try:
                p = G.order()
            except Exception:
                p = None
    except Exception:
        G = witness
        p = None

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if h1 and p is not None:
            order = int(G.order())
            p_val = int(p)
            if order == 1:
                h2 = True
            elif p_val <= 1:
                h2 = False
            else:
                val = 1
                h2 = False
                while val <= order:
                    if val == order:
                        h2 = True
                        break
                    val *= p_val
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            neg_q = not bool(G.is_solvable)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is a power of p",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2