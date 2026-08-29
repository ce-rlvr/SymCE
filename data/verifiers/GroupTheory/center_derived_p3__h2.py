import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    "H_1: G is a non-abelian group",
    "H_2: The order of G is p^3 for some integer p",
    "¬Q: The center Z(G) is not equal to the derived subgroup G'"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: G is a non-abelian group
    try:
        is_ab = witness.is_abelian
        if callable(is_ab):
            is_ab = is_ab()
            
        if is_ab is None:
            h1 = False
        else:
            h1 = not bool(is_ab)
    except Exception:
        h1 = False

    # H_2: The order of G is p^3
    try:
        order_val = witness.order() if callable(witness.order) else witness.order
        order_val = int(order_val)
        if order_val < 1:
            h2 = False
        else:
            p = int(round(order_val**(1.0/3.0)))
            h2 = (p**3 == order_val)
    except Exception:
        h2 = False

    # ¬Q: The center Z(G) is not equal to the derived subgroup G'
    try:
        Z = witness.center() if callable(witness.center) else witness.center
        D = witness.derived_subgroup() if callable(witness.derived_subgroup) else witness.derived_subgroup
        
        o1 = Z.order() if callable(Z.order) else Z.order
        o2 = D.order() if callable(D.order) else D.order
        
        if int(o1) != int(o2):
            are_equal = False
        else:
            are_equal = True
            for g in Z.generators:
                if not D.contains(g):
                    are_equal = False
                    break
                    
        neg_q = not are_equal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]