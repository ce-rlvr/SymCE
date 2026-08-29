import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation

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

def is_cyclic(grp):
    if not isinstance(grp, PermutationGroup):
        return False
    try:
        is_ab = grp.is_abelian() if callable(grp.is_abelian) else grp.is_abelian
        if not is_ab:
            return False
        order = grp.order() if callable(grp.order) else grp.order
        for g in grp.elements:
            g_order = g.order() if callable(g.order) else g.order
            if g_order == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    G = None
    H = None
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
    except Exception:
        pass

    try:
        h1_ok = is_cyclic(G)
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = isinstance(H, PermutationGroup) and not is_cyclic(H)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: H is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1