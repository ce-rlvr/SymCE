import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, oo

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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, k = witness
        else:
            G = witness
            if hasattr(G, 'order') and G.order() == oo:
                k = oo
            else:
                k = len(G.conjugacy_classes())
    except Exception:
        return [False, False]

    try:
        actual_k = None
        if hasattr(G, 'order') and G.order() == oo:
            actual_k = oo
        elif hasattr(G, 'conjugacy_classes'):
            actual_k = len(G.conjugacy_classes())
            
        h1_ok = bool((k == actual_k) and (actual_k is not None))
    except Exception:
        h1_ok = False

    try:
        if hasattr(G, 'is_abelian'):
            is_ab = bool(G.is_abelian)
        else:
            is_ab = bool(len(G.generators) <= 1)
            
        order = G.order()
        k_eq_order = bool(k == order)
        
        neg_q_ok = bool(is_ab != k_eq_order)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is the number of distinct conjugacy classes of G",
    "¬Q: G is abelian if and only if k = |G| is false"
]

N_HYP = 1
NEG_Q_INDEX = 1