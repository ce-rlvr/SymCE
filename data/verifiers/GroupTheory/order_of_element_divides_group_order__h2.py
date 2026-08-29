import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, g = witness
    except Exception:
        return [False, False]

    # H_1: G is a finite group
    try:
        # In SymPy, all PermutationGroups are finite.
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: The order of g does not divide the order of G
    try:
        order_G = G.order()
        
        if hasattr(g, 'order'):
            if callable(g.order):
                order_g = g.order()
            else:
                order_g = g.order
        else:
            order_g = None
            
        if order_g is not None and order_g > 0:
            neg_q_ok = (order_G % order_g) != 0
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The order of g does not divide the order of G"
]

N_HYP = 1
NEG_Q_INDEX = 1