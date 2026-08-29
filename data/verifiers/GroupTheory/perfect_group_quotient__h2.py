import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    try:
        G, N = witness
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and N.is_subgroup(G)
    except Exception:
        h1 = False

    try:
        G, N = witness
        h2 = G.derived_subgroup().order() == G.order()
    except Exception:
        h2 = False

    try:
        G, N = witness
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
            neg_q = False
        elif not N.is_subgroup(G):
            neg_q = True
        else:
            is_normal = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            if not is_normal:
                # If N is not normal, G/N is not a group, so it cannot be a perfect group.
                neg_q = True
            else:
                # If N is normal, check if the quotient group G/N is perfect.
                try:
                    Q = G.quotient_group(N)
                    neg_q = Q.derived_subgroup().order() != Q.order()
                except Exception:
                    # Fallback if quotient_group fails: G/N is perfect iff G = [G,G]N
                    D = G.derived_subgroup()
                    DN = PermutationGroup(*(list(D.generators) + list(N.generators)))
                    neg_q = DN.order() != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is a perfect group",
    "¬Q: G/N is not a perfect group"
]

N_HYP = 2
NEG_Q_INDEX = 2