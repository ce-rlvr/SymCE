import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def normal_closure(H, K):
    """Computes the normal closure of subgroup H in group K."""
    closure = H
    while True:
        order_before = closure.order()
        new_gens = list(closure.generators)
        for k in K.generators:
            for h in closure.generators:
                new_gens.append(~k * h * k)
                new_gens.append(k * h * ~k)
        
        unique_gens = []
        seen = set()
        for g in new_gens:
            if g not in seen:
                seen.add(g)
                unique_gens.append(g)
                
        if not unique_gens:
            unique_gens = [Permutation()]
            
        closure = PermutationGroup(unique_gens)
        if closure.order() == order_before:
            break
    return closure

def subnormal_defect(H, G):
    """
    Computes the subnormal defect of H in G.
    Returns float('inf') if H is not subnormal in G.
    """
    if not all(g in G for g in H.generators):
        return float('inf')
    if H.order() == G.order():
        return 0
        
    current = G
    defect = 0
    while True:
        next_group = normal_closure(H, current)
        defect += 1
        if next_group.order() == H.order():
            return defect
        if next_group.order() == current.order():
            return float('inf')
        current = next_group

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, H, c = witness
        elif len(witness) == 2:
            G, H = witness
            c = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        h2_ok = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        h2_ok = False

    # neg_Q: H is NOT a subnormal subgroup of G with subnormal defect at most c
    try:
        defect = subnormal_defect(H, G)
        if c is not None:
            neg_q_ok = not (defect <= c)
        else:
            neg_q_ok = math.isinf(defect)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not a subnormal subgroup of G with subnormal defect at most c"
]

N_HYP = 2
NEG_Q_INDEX = 2