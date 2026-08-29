import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.ntheory
import math

# Top-level setup for witness expressions
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

def is_subgroup(H, G):
    try:
        if H.order() > G.order():
            return False
        for h in H.generators:
            if not G.contains(h):
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(H, G):
    try:
        if not is_subgroup(H, G):
            return False
        for g in G.generators:
            g_inv = ~g
            for h in H.generators:
                if not H.contains(g * h * g_inv):
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, N, p, P = witness
    except Exception:
        return [False] * 5

    # H1: G is a finite group
    try:
        h1 = hasattr(G, 'generators') and hasattr(G, 'order') and G.order() > 0
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = is_normal_subgroup(N, G)
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = sympy.ntheory.isprime(p)
    except Exception:
        h3 = False

    # H4: P is a Sylow p-subgroup of N
    try:
        if not is_subgroup(P, N):
            h4 = False
        else:
            order_N = N.order()
            order_P = P.order()
            if order_N % order_P != 0:
                h4 = False
            else:
                m = order_N // order_P
                temp = order_P
                is_p_group = True
                while temp > 1:
                    if temp % p != 0:
                        is_p_group = False
                        break
                    temp //= p
                if is_p_group and math.gcd(int(m), int(p)) == 1:
                    h4 = True
                else:
                    h4 = False
    except Exception:
        h4 = False

    # ¬Q: P is not a normal subgroup of G
    try:
        neg_q = not is_normal_subgroup(P, G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: p is a prime number",
    "H_4: P is a Sylow p-subgroup of N",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4