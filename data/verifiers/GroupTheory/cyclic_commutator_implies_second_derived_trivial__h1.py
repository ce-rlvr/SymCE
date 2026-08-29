import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G_prime = witness.derived_subgroup()
        h1_ok = False
        fallback = False
        
        if hasattr(G_prime, 'is_cyclic'):
            val = G_prime.is_cyclic
            if callable(val):
                h1_ok = bool(val())
            elif val is not None:
                h1_ok = bool(val)
            else:
                fallback = True
        else:
            fallback = True
            
        if fallback:
            order_attr = G_prime.order
            if callable(order_attr):
                order_val = order_attr()
            else:
                order_val = order_attr
                
            for g in G_prime.elements:
                g_order = g.order
                if callable(g_order):
                    g_val = g_order()
                else:
                    g_val = g_order
                if g_val == order_val:
                    h1_ok = True
                    break
    except Exception:
        h1_ok = False

    try:
        G_prime = witness.derived_subgroup()
        G_prime_prime = G_prime.derived_subgroup()
        
        order_attr = G_prime_prime.order
        if callable(order_attr):
            val = order_attr()
        else:
            val = order_attr
            
        neg_q_ok = not (val == 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G' is a cyclic group",
    "¬Q: G'' is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1