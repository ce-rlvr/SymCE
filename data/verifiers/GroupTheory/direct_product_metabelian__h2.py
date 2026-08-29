import sympy
from sympy.combinatorics import (
    PermutationGroup,
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup
)
try:
    from sympy.combinatorics import DirectProduct
except ImportError:
    DirectProduct = None

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_metabelian(G):
    if not hasattr(G, 'derived_subgroup'):
        return False
    try:
        D = G.derived_subgroup()
        return bool(D.is_abelian)
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = h1 and is_metabelian(H)
    except Exception:
        h2 = False

    try:
        if h1:
            if DirectProduct is not None:
                try:
                    GxH = DirectProduct(G, H)
                    neg_q = not is_metabelian(GxH)
                except Exception:
                    neg_q = not (is_metabelian(G) and is_metabelian(H))
            else:
                neg_q = not (is_metabelian(G) and is_metabelian(H))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: H is a metabelian group",
    r"¬Q: G \times H is not a metabelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2