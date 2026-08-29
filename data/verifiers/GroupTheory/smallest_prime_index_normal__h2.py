import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def get_order(grp):
    try:
        return grp.order()
    except TypeError:
        return grp.order

def check_subgroup(H, G):
    try:
        return bool(H.is_subgroup(G))
    except Exception:
        for h in H.generators:
            if h not in G:
                return False
        return True

def check_normal(G, H):
    try:
        return bool(G.is_normal(H))
    except Exception:
        for g in G.generators:
            for h in H.generators:
                if (g * h * ~g) not in H:
                    return False
        return True

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and check_subgroup(H, G)
    except Exception:
        h2 = False

    # H3: The index of H in G is equal to p
    try:
        if h1 and h2:
            g_order = get_order(G)
            h_order = get_order(H)
            if h_order > 0 and g_order % h_order == 0:
                idx = g_order // h_order
                h3 = bool(isprime(idx))
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: H is not a normal subgroup of G
    try:
        if h1 and h2:
            neg_q = not check_normal(G, H)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: The index of H in G is equal to p",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3