import sympy
from sympy.combinatorics.free_groups import free_group, FreeGroup, FreeGroupElement
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

F2, x, y = free_group("x, y")
F3, a, b, c = free_group("a, b, c")

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, g = witness
        else:
            F = getattr(witness, "group", None)
            g = witness
    except Exception:
        F, g = None, None

    try:
        h1 = isinstance(F, FreeGroup) and isinstance(g, FreeGroupElement) and g.group == F
    except Exception:
        h1 = False

    try:
        if h1:
            neg_q = bool(g == F.identity)
        else:
            if hasattr(F, 'identity'):
                neg_q = bool(g == F.identity)
            elif hasattr(g, 'is_identity'):
                neg_q = bool(g.is_identity)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: g belongs to all normal subgroups of finite index (g is the identity)"
]

N_HYP = 1
NEG_Q_INDEX = 1