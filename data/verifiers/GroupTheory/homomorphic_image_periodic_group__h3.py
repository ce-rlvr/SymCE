import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

class Z_Group:
    def __repr__(self):
        return "Z"
Z = Z_Group()

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
        G, H, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        def check_group(grp):
            if grp is Z or grp is sympy.S.Integers:
                return True
            if isinstance(grp, PermutationGroup):
                return True
            return False
        h1 = check_group(G) and check_group(H)
    except Exception:
        h1 = False
        
    # H_2: f is a group homomorphism
    try:
        h2 = False
        if h1:
            def H_op(a, b):
                if H is Z or H is sympy.S.Integers:
                    return a + b
                else:
                    return a * b
            
            def apply_f(val):
                if callable(f):
                    return f(val)
                return f[val]
                
            def in_H(val):
                if H is Z or H is sympy.S.Integers:
                    return isinstance(val, (int, sympy.Integer))
                else:
                    return val in H.elements

            is_hom = True
            if G is Z or G is sympy.S.Integers:
                for x in [-2, -1, 0, 1, 2]:
                    fx = apply_f(x)
                    if not in_H(fx):
                        is_hom = False
                        break
                    for y in [-2, -1, 0, 1, 2]:
                        if apply_f(x + y) != H_op(fx, apply_f(y)):
                            is_hom = False
                            break
                    if not is_hom:
                        break
            else:
                elements = list(G.elements)
                for x in elements:
                    fx = apply_f(x)
                    if not in_H(fx):
                        is_hom = False
                        break
                    for y in elements:
                        if apply_f(x * y) != H_op(fx, apply_f(y)):
                            is_hom = False
                            break
                    if not is_hom:
                        break
            h2 = is_hom
    except Exception:
        h2 = False
        
    # neg_Q: f(G) is NOT a periodic group
    try:
        neg_q = False
        if h1 and h2:
            def apply_f(val):
                if callable(f):
                    return f(val)
                return f[val]

            if G is Z or G is sympy.S.Integers:
                if H is Z or H is sympy.S.Integers:
                    # In Z, only 0 has finite order. If f(1) != 0, the image contains elements of infinite order.
                    if apply_f(1) != 0:
                        neg_q = True
                else:
                    # H is a PermutationGroup, all elements have finite order
                    neg_q = False
            else:
                # G is finite, so f(G) is finite, hence periodic
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "¬Q: The image f(G) is not a periodic group"
]

N_HYP = 2
NEG_Q_INDEX = 2