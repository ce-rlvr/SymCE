import sympy
from sympy.combinatorics import PermutationGroup, DirectProduct
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
V4 = DirectProduct(CyclicGroup(2), CyclicGroup(2))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: H is non-trivial
    try:
        h2 = h1 and H.order() > 1
    except Exception:
        h2 = False
        
    # neg_Q: G \times H is subdirectly irreducible
    try:
        if not h1:
            neg_q = False
        else:
            GH = DirectProduct(G, H)
            if GH.order() == 1:
                neg_q = False
            else:
                normal_subgroups = GH.normal_subgroups()
                non_trivial_ns = [ns for ns in normal_subgroups if ns.order() > 1]
                if not non_trivial_ns:
                    neg_q = False
                else:
                    intersection = set(non_trivial_ns[0].elements)
                    for ns in non_trivial_ns[1:]:
                        intersection = intersection.intersection(set(ns.elements))
                    neg_q = len(intersection) > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: H is non-trivial",
    "¬Q: G \\times H is subdirectly irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2