import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(grp):
    o = grp.order
    if callable(o):
        return o()
    return o

def get_derived_subgroup(grp):
    ds = grp.derived_subgroup
    if callable(ds):
        return ds()
    return ds

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H1: G and N are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if h1:
            is_subgroup = True
            for gen in N.generators:
                if gen not in G:
                    is_subgroup = False
                    break
            
            is_normal = True
            if is_subgroup:
                for n in N.generators:
                    for g in G.generators:
                        if (g**-1) * n * g not in N:
                            is_normal = False
                            break
                        if g * n * (g**-1) not in N:
                            is_normal = False
                            break
            else:
                is_normal = False
                
            h2 = is_subgroup and is_normal
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: N is a perfect group
    try:
        if h1:
            h3 = get_order(get_derived_subgroup(N)) == get_order(N)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: G is not a perfect group
    try:
        if h1:
            neg_q = get_order(get_derived_subgroup(G)) != get_order(G)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and N are groups",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a perfect group",
    "¬Q: G is not a perfect group"
]

N_HYP = 3
NEG_Q_INDEX = 3