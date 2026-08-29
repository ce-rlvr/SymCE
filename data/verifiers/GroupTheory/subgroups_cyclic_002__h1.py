import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return bool(H.is_subgroup(G))
    except Exception:
        pass
    try:
        return all(G.contains(g) for g in H.generators)
    except Exception:
        return False

def is_cyclic(group):
    try:
        if hasattr(group, 'is_cyclic'):
            res = group.is_cyclic
            if res is not None:
                return bool(res)
    except Exception:
        pass
    try:
        order = group.order()
        for g in group.generate():
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G', witness.get('H'))
            H = witness.get('H', G)
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = witness
    except Exception:
        return [False, False]

    # H_1: H is a subgroup of G
    try:
        h1_ok = is_subgroup(H, G)
    except Exception:
        h1_ok = False

    # ¬Q: H is not a cyclic group
    try:
        neg_q_ok = not is_cyclic(H)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: H is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1