import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime, factorint
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        G, p, H, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: H is a p-subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h_in_g = all(gen in G for gen in H.generators)
            order_H = H.order()
            factors = factorint(order_H)
            is_p_group = (order_H == 1) or (list(factors.keys()) == [p])
            h3 = bool(h_in_g and is_p_group)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: H is not a subgroup of gPg^(-1) for any g in G
    try:
        if isinstance(P, PermutationGroup) and isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            exists_g = False
            for g in G.elements:
                if all((~g * h * g) in P for h in H.generators):
                    exists_g = True
                    break
            neg_q = not exists_g
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: H is a p-subgroup of G",
    "¬Q: H is not a subgroup of gPg^(-1) for any g in G"
]

N_HYP = 3
NEG_Q_INDEX = 3