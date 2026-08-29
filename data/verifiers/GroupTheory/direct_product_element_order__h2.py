import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup: named object bindings
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
        if len(witness) == 4:
            G, H, g, h = witness
            m = g.order() if hasattr(g, 'order') else 1
            n = h.order() if hasattr(h, 'order') else 1
        elif len(witness) == 6:
            G, H, g, h, m, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: h is an element of H with finite order n
    try:
        h2 = isinstance(h, Permutation) and (h in H) and (h.order() == n)
    except Exception:
        h2 = False

    # neg_Q: The order of the element (g, h) in the direct product G \times H is the least common multiple of m and n
    try:
        if not isinstance(g, Permutation) or not isinstance(h, Permutation):
            q = False
        elif g not in G or h not in H:
            q = False
        elif not isinstance(m, int) or not isinstance(n, int):
            q = False
        else:
            actual_order = math.lcm(g.order(), h.order())
            expected_order = math.lcm(m, n)
            q = (actual_order == expected_order)
        neg_q = not q
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: h is an element of H with finite order n",
    "¬Q: The order of the element (g, h) in the direct product G \\times H is not the least common multiple of m and n"
]

N_HYP = 2
NEG_Q_INDEX = 2