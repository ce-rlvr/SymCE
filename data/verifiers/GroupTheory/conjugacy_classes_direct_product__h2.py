import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    "H_1: G and H are groups",
    "H_2: h is an element of H",
    "¬Q: The conjugacy class of (g, h) in G x H is not the Cartesian product of the conjugacy classes (e.g., because g is not in G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            g = witness.get('g')
            h = witness.get('h')
        else:
            G, H, g, h = witness
    except Exception:
        return [False, False, False]
        
    def is_group(obj):
        if isinstance(obj, PermutationGroup):
            return True
        if hasattr(obj, 'generators') or hasattr(obj, 'elements'):
            return True
        return False
        
    try:
        h1 = bool(is_group(G) and is_group(H))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(h in H)
    except Exception:
        h2 = False
        
    try:
        in_G = bool(g in G)
        in_H = bool(h in H)
        # The conclusion holds if g is in G and h is in H.
        # It fails if g is not in G, because the conjugacy class of g in G is undefined.
        conclusion = in_G and in_H
        neg_q = not conclusion
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]