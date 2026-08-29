import math
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The order of N and the index of N in G are coprime",
    "H_3: H1 and H2 are two complements of N in G",
    "¬Q: H1 and H2 are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, N, H1, H2 = witness
    except Exception:
        return [False, False, False, False]
    
    def is_subgroup(sub, parent):
        try:
            return all(parent.contains(g) for g in sub.generators)
        except Exception:
            return False

    # H_1: N is a normal subgroup of G
    try:
        h1_ok = False
        if is_subgroup(N, G):
            is_normal = True
            for g in G.generators:
                g_inv = g**-1
                for n in N.generators:
                    if not N.contains(g * n * g_inv):
                        is_normal = False
                        break
                if not is_normal:
                    break
            h1_ok = is_normal
    except Exception:
        h1_ok = False

    # H_2: The order of N and the index of N in G are coprime
    try:
        h2_ok = False
        order_N = int(N.order())
        order_G = int(G.order())
        if order_G % order_N == 0:
            index = order_G // order_N
            h2_ok = (math.gcd(order_N, index) == 1)
    except Exception:
        h2_ok = False

    # H_3: H1 and H2 are two complements of N in G
    try:
        h3_ok = False
        if is_subgroup(H1, G) and is_subgroup(H2, G):
            order_H1 = int(H1.order())
            order_H2 = int(H2.order())
            order_N = int(N.order())
            order_G = int(G.order())
            # For a normal subgroup N, H is a complement iff |N|*|H| = |G| and H is a subgroup
            if order_N * order_H1 == order_G and order_N * order_H2 == order_G:
                h3_ok = True
    except Exception:
        h3_ok = False

    # ¬Q: H1 and H2 are not conjugate in G
    try:
        neg_q = False
        if int(H1.order()) == int(H2.order()):
            are_conj = False
            gens1 = H1.generators
            # Since G = N H1 and H1 normalizes itself, any conjugate of H1 in G 
            # is of the form n H1 n^-1 for some n in N.
            for n in N.generate():
                n_inv = n**-1
                if all(H2.contains(n * h * n_inv) for h in gens1):
                    are_conj = True
                    break
            neg_q = not are_conj
        else:
            # If they don't have the same order, they cannot be conjugate
            neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]