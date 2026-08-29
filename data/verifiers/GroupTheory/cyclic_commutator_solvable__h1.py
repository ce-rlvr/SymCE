import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def is_cyclic(G):
    try:
        if hasattr(G, 'is_cyclic'):
            val = G.is_cyclic
            if callable(val):
                return bool(val())
            elif val is not None:
                return bool(val)
    except Exception:
        pass
    
    try:
        order = G.order
        if callable(order):
            order = order()
        if order == 1:
            return True
        for g in G.elements:
            g_order = g.order
            if callable(g_order):
                g_order = g_order()
            if g_order == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        G_prime = witness.derived_subgroup()
        h1_ok = bool(is_cyclic(G_prime))
    except Exception:
        h1_ok = False

    try:
        solvable = witness.is_solvable
        if callable(solvable):
            solvable = solvable()
        neg_q = not bool(solvable)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: The commutator subgroup G' is cyclic",
    "¬Q: The group G is not solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1