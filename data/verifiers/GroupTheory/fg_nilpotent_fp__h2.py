import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "Every nilpotent group is finitely presented."
    """
    # H_1: G is a nilpotent group
    h1_ok = False
    try:
        if hasattr(witness, 'is_nilpotent'):
            val = witness.is_nilpotent
            h1_ok = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'is_abelian'):
            val = witness.is_abelian
            h1_ok = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'lower_central_series'):
            lcs = witness.lower_central_series()
            h1_ok = (len(lcs) > 0 and lcs[-1].is_trivial)
    except Exception:
        h1_ok = False

    # neg_Q: G is not a finitely presented group
    neg_q_ok = False
    try:
        is_fp = None
        if hasattr(witness, 'is_finitely_presented'):
            val = witness.is_finitely_presented
            is_fp = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'is_finitely_generated'):
            val = witness.is_finitely_generated
            is_fg = bool(val()) if callable(val) else bool(val)
            if not is_fg:
                is_fp = False
        
        if is_fp is None:
            class_name = type(witness).__name__
            if isinstance(witness, PermutationGroup) or class_name in ('FpGroup', 'FreeGroup'):
                is_fp = True
                
        if is_fp is not None:
            neg_q_ok = not is_fp
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G is not a finitely presented group"
]

N_HYP = 1
NEG_Q_INDEX = 1