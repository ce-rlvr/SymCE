import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
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

def conditions(witness):
    G, H, x = None, None, None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            x = witness.get('x')
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, x = witness
            elif len(witness) == 4:
                G, _, H, x = witness
    except Exception:
        pass

    # H_1: H is a subgroup of G
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False

    # H_2: x is an element of X
    try:
        if isinstance(x, (int, sympy.Integer)):
            h2 = (0 <= x < G.degree)
        else:
            h2 = all(isinstance(i, (int, sympy.Integer)) and 0 <= i < G.degree for i in x)
    except Exception:
        h2 = False

    # neg_Q: Stab_H(x) != H \cap Stab_G(x)
    try:
        stab_H = H.stabilizer(x)
        stab_G = G.stabilizer(x)
        
        if hasattr(H, 'intersect'):
            intersection = H.intersect(stab_G)
        elif hasattr(H, 'intersection'):
            intersection = H.intersection(stab_G)
        else:
            int_elements = set(H.elements).intersection(set(stab_G.elements))
            intersection = PermutationGroup(list(int_elements))
            
        is_equal = (stab_H.order() == intersection.order()) and stab_H.is_subgroup(intersection)
        neg_q = not is_equal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: x is an element of X",
    "¬Q: Stab_H(x) != H \\cap Stab_G(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2