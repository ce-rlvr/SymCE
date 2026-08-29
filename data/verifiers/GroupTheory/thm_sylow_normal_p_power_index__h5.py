import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def is_subgroup(H, G):
    try:
        return all(G.contains(h) for h in H.generators)
    except Exception:
        return False

def is_normal(N, G):
    try:
        if not is_subgroup(N, G):
            return False
        for g in G.generators:
            g_inv = ~g
            for n in N.generators:
                if not N.contains(g * n * g_inv):
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, p, P, N = witness
    except Exception:
        return [False] * 5
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    # H2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False
        
    # H3: P is a Sylow p-subgroup of G
    try:
        p_int = int(p)
        if p_int <= 1 or p_int != p:
            h3 = False
        elif not is_subgroup(P, G):
            h3 = False
        else:
            order_P = P.order()
            order_G = G.order()
            if order_P == 1:
                h3 = (order_G % p_int != 0)
            else:
                temp = order_P
                while temp % p_int == 0:
                    temp //= p_int
                if temp != 1:
                    h3 = False
                else:
                    index = order_G // order_P
                    h3 = (index % p_int != 0)
    except Exception:
        h3 = False
        
    # H4: N is a normal subgroup of G
    try:
        h4 = is_normal(N, G)
    except Exception:
        h4 = False
        
    # neg_Q: G != PN
    try:
        gens = list(P.generators) + list(N.generators)
        PN = PermutationGroup(gens)
        neg_q = PN.order() != G.order()
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: N is a normal subgroup of G",
    "¬Q: G != PN"
]

N_HYP = 4
NEG_Q_INDEX = 4