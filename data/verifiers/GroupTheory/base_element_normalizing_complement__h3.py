import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, N, H, n = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group that is the internal semidirect product of a normal subgroup N and a subgroup H
    try:
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            is_subgroups = N.is_subgroup(G) and H.is_subgroup(G)
            is_normal = N.is_normal(G)
            
            try:
                N_elems = set(N.elements)
            except Exception:
                N_elems = set(N.generate())
                
            try:
                H_elems = set(H.elements)
            except Exception:
                H_elems = set(H.generate())
                
            # Internal semidirect product requires N \cap H = {e} and |N| * |H| = |G|
            intersect_trivial = len(N_elems.intersection(H_elems)) == 1
            
            try:
                g_order = G.order()
                n_order = N.order()
                h_order = H.order()
            except Exception:
                g_order = len(list(G.generate()))
                n_order = len(N_elems)
                h_order = len(H_elems)
                
            order_correct = (n_order * h_order == g_order)
            
            h1 = bool(is_subgroups and is_normal and intersect_trivial and order_correct)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: n is an element of N
    try:
        try:
            N_elems = set(N.elements)
        except Exception:
            N_elems = set(N.generate())
        h2 = bool(n in N_elems)
    except Exception:
        h2 = False

    # ¬Q: There exists h in H such that n h n^{-1} != h (equivalent to n h != h n)
    try:
        try:
            H_elems = set(H.elements)
        except Exception:
            H_elems = set(H.generate())
        neg_q = bool(any(n * h != h * n for h in H_elems))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group that is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: n is an element of N",
    "¬Q: There exists h in H such that n h n^{-1} != h"
]

N_HYP = 2
NEG_Q_INDEX = 2