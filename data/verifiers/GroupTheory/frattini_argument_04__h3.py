import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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

def conditions(witness) -> list[bool]:
    try:
        G, H, P = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1_ok = False

    try:
        h2_ok = H.is_subgroup(G) and H.is_normal(G)
    except Exception:
        h2_ok = False

    try:
        P_elements = set(P.elements)
        N_G_P = []
        for g in G.elements:
            g_inv = ~g
            if all((g * p * g_inv) in P_elements for p in P_elements):
                N_G_P.append(g)
        
        HN_elements = set()
        for h in H.elements:
            for n in N_G_P:
                HN_elements.add(h * n)
                
        neg_q_ok = len(HN_elements) != G.order()
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a normal subgroup of G",
    "¬Q: G != H N_G(P)"
]

N_HYP = 2
NEG_Q_INDEX = 2