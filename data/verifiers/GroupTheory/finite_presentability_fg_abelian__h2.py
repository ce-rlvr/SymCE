import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Handle known string counterexamples
    if isinstance(witness, str):
        name = witness.lower().replace(" ", "").replace("_", "").replace("-", "")
        fg_not_fp = ["lamplightergroup", "z2wrz", "zwrz", "grigorchukgroup", "grigorchuk", "baumslaagsolitar", "bs(2,3)"]
        if name in fg_not_fp:
            return [True, True]
            
    # H_1: G is a finitely generated group
    try:
        if hasattr(witness, 'is_finitely_generated'):
            val = witness.is_finitely_generated
            h1 = val() if callable(val) else bool(val)
        elif isinstance(witness, PermutationGroup):
            h1 = True
        elif type(witness).__name__ in ('FpGroup', 'FreeGroup'):
            h1 = True
        elif hasattr(witness, 'generators'):
            h1 = hasattr(witness.generators, '__len__')
    except Exception:
        h1 = False

    # ¬Q: G is not finitely presented
    try:
        if hasattr(witness, 'is_finitely_presented'):
            val = witness.is_finitely_presented
            is_fp = val() if callable(val) else bool(val)
        elif isinstance(witness, PermutationGroup):
            is_fp = True
        elif type(witness).__name__ in ('FpGroup', 'FreeGroup'):
            is_fp = True
        elif hasattr(witness, 'relators'):
            is_fp = hasattr(witness.relators, '__len__')
        else:
            # Default to True (finitely presented) so neg_q is False if we cannot determine
            is_fp = True 
            
        neg_q = not is_fp
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "¬Q: G is not finitely presented"
]

N_HYP = 1
NEG_Q_INDEX = 1