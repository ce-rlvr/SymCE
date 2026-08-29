import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import factorint

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
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a finite p-group
    try:
        order_G = G.order()
        factors_G = factorint(order_G)
        # A finite group is a p-group if its order is a prime power (or 1 for the trivial p-group)
        h1 = len(factors_G) <= 1
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        is_subgroup = all(G.contains(gen) for gen in N.generators)
        is_normal = all(N.contains(g * n * ~g) for g in G.generators for n in N.generators)
        h2 = bool(is_subgroup and is_normal)
    except Exception:
        h2 = False

    # ¬Q: The quotient group G/N is not a p-group
    try:
        order_G = G.order()
        order_N = N.order()
        if order_G % order_N != 0:
            neg_q = False
        else:
            order_quotient = order_G // order_N
            factors_quotient = factorint(order_quotient)
            is_p_group = len(factors_quotient) <= 1
            neg_q = not is_p_group
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The quotient group G/N is not a p-group"
]

N_HYP = 2
NEG_Q_INDEX = 2