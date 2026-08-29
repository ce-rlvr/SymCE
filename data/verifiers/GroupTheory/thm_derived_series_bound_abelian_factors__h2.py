import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def is_subgroup(H, G):
    if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    return all(g in G for g in H.generators)

def is_normal(H, G):
    if not is_subgroup(H, G):
        return False
    for g in G.generators:
        for h in H.generators:
            if (g * h * g**-1) not in H:
                return False
    return True

def quotient_is_abelian(H, G):
    if not is_subgroup(H, G):
        return False
    for x in G.generators:
        for y in G.generators:
            if (x * y * x**-1 * y**-1) not in H:
                return False
    return True

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, series = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: series is a subnormal series with abelian factor groups
    try:
        if not isinstance(series, list) or len(series) < 1:
            h2 = False
        else:
            h2 = True
            # Check G == series[0]
            if not (is_subgroup(G, series[0]) and is_subgroup(series[0], G)):
                h2 = False
            else:
                for i in range(len(series) - 1):
                    H = series[i+1]
                    K = series[i]
                    if not is_normal(H, K):
                        h2 = False
                        break
                    if not quotient_is_abelian(H, K):
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # neg_Q: G^(n) is NOT trivial
    try:
        if h1 and isinstance(series, list) and len(series) >= 1:
            n = len(series) - 1
            Gn = G
            for _ in range(n):
                Gn = Gn.derived_subgroup()
            neg_q = (Gn.order() > 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: All factor groups of this subnormal series are abelian",
    "¬Q: The n-th term of the derived series, G^(n), is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2