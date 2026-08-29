import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import primefactors

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
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, p, H = witness
            elif len(witness) == 2:
                G, H = witness
                try:
                    p = primefactors(G.order())[0]
                except Exception:
                    p = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is the smallest prime number dividing the order of G
    try:
        if h1 and G.order() > 1:
            factors = primefactors(G.order())
            h2 = (p == factors[0])
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h3 = False

    # neg_Q: H is not a normal subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            neg_q = not H.is_normal(G)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is the smallest prime number dividing the order of G",
    "H_3: H is a subgroup of G",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3