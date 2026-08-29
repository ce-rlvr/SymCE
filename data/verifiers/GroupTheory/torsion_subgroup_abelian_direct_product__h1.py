import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def _is_abelian(grp):
    if hasattr(grp, 'is_abelian'):
        return grp.is_abelian
    if isinstance(grp, (list, tuple)):
        for a, b in itertools.product(grp, grp):
            if a * b != b * a:
                return False
        return True
    return False

def _torsion_is_subgroup(grp):
    if hasattr(grp, 'torsion_is_subgroup'):
        return grp.torsion_is_subgroup()
    if hasattr(grp, 'is_abelian') and grp.is_abelian:
        return True
    if isinstance(grp, (list, tuple)):
        finite_elems = []
        for M in grp:
            P = M
            is_fin = False
            for _ in range(1, 20):
                if P == eye(M.shape[0]):
                    is_fin = True
                    break
                P = P * M
            if is_fin:
                finite_elems.append(M)
        for A, B in itertools.product(finite_elems, finite_elems):
            AB = A * B
            P = AB
            is_fin = False
            for _ in range(1, 40):
                if P == eye(A.shape[0]):
                    is_fin = True
                    break
                P = P * AB
            if not is_fin:
                return False
        return True
    return True

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(_is_abelian(H))
    except Exception:
        h1_ok = False

    try:
        q_ok = bool(_torsion_is_subgroup(G) and _torsion_is_subgroup(H))
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is an abelian group",
    "¬Q: T(G x H) is not equal to T(G) x T(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1