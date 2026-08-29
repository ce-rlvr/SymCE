import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

try:
    from sympy.combinatorics.free_groups import free_group
    from sympy.combinatorics.fp_groups import FpGroup
except ImportError:
    pass

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: G is a finitely presented group",
    "¬Q: G is not an infinite group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # H_1: G is a finitely presented group
    try:
        is_fp = False
        # Every finite group (PermutationGroup) is finitely presented.
        if isinstance(witness, PermutationGroup):
            is_fp = True
        elif type(witness).__name__ == 'FpGroup':
            is_fp = True
        elif type(witness).__name__ == 'FreeGroup':
            is_fp = len(witness.generators) < float('inf')
        h1_ok = bool(is_fp)
    except Exception:
        h1_ok = False

    # ¬Q: G is not an infinite group (i.e., G is finite)
    try:
        neg_q_ok = False
        if hasattr(witness, 'order'):
            ord_G = witness.order()
            neg_q_ok = (ord_G != sympy.oo)
        elif hasattr(witness, 'is_finite'):
            neg_q_ok = bool(witness.is_finite)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]