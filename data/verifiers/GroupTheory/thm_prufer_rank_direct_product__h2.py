import sympy
import sympy.combinatorics as combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
from sympy.matrices import eye, zeros
from sympy import oo

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(grp):
    if isinstance(grp, combinatorics.PermutationGroup):
        return True
    cls_name = type(grp).__name__
    if cls_name in ('FreeGroup', 'FpGroup'):
        return True
    return False

def has_finite_prufer_rank(grp):
    if isinstance(grp, combinatorics.PermutationGroup):
        return True
    cls_name = type(grp).__name__
    if cls_name == 'FreeGroup':
        return len(grp.generators) <= 1
    if cls_name == 'FpGroup':
        if len(grp.generators) <= 1:
            return True
        try:
            return grp.order() != oo
        except Exception:
            return False
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a group of finite Prufer rank
    try:
        h1_ok = is_group(G) and has_finite_prufer_rank(G)
    except Exception:
        h1_ok = False

    # ¬Q: The direct product G x H is NOT a group of finite Prufer rank
    # G x H has finite Prufer rank iff both G and H have finite Prufer rank.
    try:
        neg_q_ok = is_group(H) and not (has_finite_prufer_rank(G) and has_finite_prufer_rank(H))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group of finite Prufer rank",
    "¬Q: The direct product G x H is not a group of finite Prufer rank"
]

N_HYP = 1
NEG_Q_INDEX = 1