import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def _get_order(grp):
    if hasattr(grp, 'order'):
        o = grp.order
        return o() if callable(o) else o
    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group and H is a subgroup of G
    try:
        h1 = False
        if _get_order(G) is not None and _get_order(H) is not None:
            if hasattr(H, 'is_subgroup'):
                h1 = bool(H.is_subgroup(G))
            elif hasattr(H, 'generators'):
                h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    # H_2: The index of H in G is exactly 2
    try:
        g_order = _get_order(G)
        h_order = _get_order(H)
        h2 = (g_order is not None and h_order is not None and g_order == 2 * h_order)
    except Exception:
        h2 = False

    # H_3: H is an abelian group
    try:
        h3 = False
        if hasattr(H, 'is_abelian'):
            val = H.is_abelian
            if callable(val):
                val = val()
            h3 = bool(val)
    except Exception:
        h3 = False

    # not Q: G is not a solvable group
    try:
        neg_q = False
        if hasattr(G, 'is_solvable'):
            val = G.is_solvable
            if callable(val):
                val = val()
            neg_q = (val is False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and H is a subgroup of G",
    "H_2: The index of H in G is exactly 2",
    "H_3: H is an abelian group",
    "not Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3