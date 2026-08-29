import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    try:
        h3 = False
        if isinstance(P, PermutationGroup) and isinstance(G, PermutationGroup) and isinstance(p, (int, sympy.Integer)) and p >= 2:
            is_subgroup = False
            try:
                is_subgroup = all(g in G for g in P.generators)
            except Exception:
                is_subgroup = False
                
            if is_subgroup:
                order_P = P.order()
                temp = order_P
                if temp > 0:
                    while temp % p == 0:
                        temp //= p
                    if temp == 1:
                        h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = False
        if not isinstance(G, PermutationGroup) or not isinstance(P, PermutationGroup) or not isinstance(p, (int, sympy.Integer)):
            neg_q = True
        elif p < 2:
            neg_q = True
        else:
            is_subgroup = False
            try:
                is_subgroup = all(g in G for g in P.generators)
            except Exception:
                is_subgroup = False
                
            if not is_subgroup:
                neg_q = True
            else:
                order_G = G.order()
                order_P = P.order()
                
                temp = order_P
                is_p_subgroup = False
                if temp > 0:
                    while temp % p == 0:
                        temp //= p
                    if temp == 1:
                        is_p_subgroup = True
                
                if not is_p_subgroup:
                    neg_q = True
                elif order_G % order_P != 0:
                    neg_q = True
                else:
                    if (order_G // order_P) % p == 0:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a subgroup of G such that the order of P is a power of p",
    "¬Q: P is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3