import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            k = witness.get('k')
            G = witness.get('G')
        else:
            k, G = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(k, int) or isinstance(k, sympy.Integer)) and k >= 1
    except Exception:
        h1 = False

    try:
        neg_q = False
        if hasattr(G, 'order'):
            order = G.order()
            # If G is a finite group, we can check if it admits the presentation.
            # For k = 1, the presentation defines Z_2 (order 2).
            # For k >= 2, the presentation defines an infinite group.
            if order != sympy.oo:
                if k == 1:
                    if order != 2:
                        neg_q = True
                elif k >= 2:
                    # A finite group cannot be isomorphic to the infinite group P_k
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N_k is a closed, connected, non-orientable surface of genus k >= 1",
    "¬Q: G does not admit the presentation < a_1, ..., a_k | a_1^2 ... a_k^2 = 1 >"
]

N_HYP = 1
NEG_Q_INDEX = 1