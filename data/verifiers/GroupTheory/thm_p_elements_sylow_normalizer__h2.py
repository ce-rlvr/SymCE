import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

def conditions(witness) -> list[bool]:
    try:
        G, P, x, p = witness
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        p_val = int(p)
        if p_val <= 1:
            h2 = False
        elif not isinstance(P, PermutationGroup):
            h2 = False
        else:
            is_sub = True
            try:
                if not P.is_subgroup(G):
                    is_sub = False
            except Exception:
                # Fallback if is_subgroup fails
                for g in P.generators:
                    if g not in G:
                        is_sub = False
                        break
            
            if not is_sub:
                h2 = False
            else:
                order_G = G.order()
                k = 0
                while order_G % (p_val**(k+1)) == 0:
                    k += 1
                h2 = (P.order() == p_val**k)
    except Exception:
        h2 = False

    # H_3: x is an element of the normalizer N_G(P)
    try:
        if x not in G:
            h3 = False
        else:
            h3 = True
            for y in P.generators:
                if (x * y * (~x)) not in P:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # H_4: The order of x is a power of p
    try:
        p_val = int(p)
        if p_val <= 1:
            h4 = False
        else:
            order_x = x.order()
            temp = order_x
            while temp % p_val == 0 and temp > 1:
                temp //= p_val
            h4 = (temp == 1)
    except Exception:
        h4 = False

    # ¬Q: The element x does not belong to P
    try:
        neg_q = x not in P
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: x is an element of the normalizer N_G(P)",
    "H_4: The order of x is a power of p",
    "¬Q: The element x does not belong to P"
]

N_HYP = 4
NEG_Q_INDEX = 4