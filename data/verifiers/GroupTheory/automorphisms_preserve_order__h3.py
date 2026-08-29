import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        if len(witness) == 3:
            G, g, phi = witness
        elif len(witness) == 4:
            G, g, n_wit, phi = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or hasattr(G, 'is_group')
    except Exception:
        h1 = False

    # H_2: g is an element of G having finite order n
    try:
        h2 = g in G and g.order() > 0
    except Exception:
        h2 = False

    # ¬Q: phi(g) does not have order exactly n in G
    try:
        n = g.order()
        if isinstance(phi, dict):
            phig = phi[g]
        elif isinstance(phi, (list, tuple)):
            if len(phi) > 0 and isinstance(phi[0], tuple) and len(phi[0]) == 2:
                phig = dict(phi)[g]
            else:
                phig = phi[g]
        else:
            phig = phi(g)
            
        if phig in G:
            neg_q = phig.order() != n
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G having finite order n",
    "¬Q: phi(g) does not have order exactly n in G"
]

N_HYP = 2
NEG_Q_INDEX = 2