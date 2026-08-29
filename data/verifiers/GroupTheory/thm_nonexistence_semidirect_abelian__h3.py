import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if len(witness) == 3:
            G, N, H = witness
        elif len(witness) == 2:
            G, N = witness
            H = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H1: G is a semisimple finite group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            h1 = True
            for ns in G.normal_subgroups():
                if ns.is_abelian and ns.order() > 1:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: N is an abelian normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup):
            if N.order() == 1:
                h2 = True
            elif N.is_subgroup(G) and N.is_abelian and N.is_normal(G):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: N is not the trivial subgroup OR H != G
    try:
        n_is_trivial = (N.order() == 1)
        try:
            if H is None:
                h_equals_g = False
            elif H.order() != G.order():
                h_equals_g = False
            else:
                h_equals_g = H.is_subgroup(G) and G.is_subgroup(H)
        except Exception:
            h_equals_g = (H == G)
        
        q = n_is_trivial and h_equals_g
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: N is an abelian normal subgroup of G",
    "¬Q: N is not the trivial subgroup or H != G"
]

N_HYP = 2
NEG_Q_INDEX = 2