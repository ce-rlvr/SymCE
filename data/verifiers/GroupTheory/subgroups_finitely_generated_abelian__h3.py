import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide two groups, G and H.
    """
    # Extract G and H from the witness
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
    elif hasattr(witness, 'G') and hasattr(witness, 'H'):
        G = witness.G
        H = witness.H
    else:
        try:
            G, H = witness
        except Exception:
            return [False, False, False]
            
    def is_group(obj):
        if hasattr(obj, 'is_group'):
            return bool(obj.is_group)
        tname = type(obj).__name__
        if tname in ('PermutationGroup', 'FreeGroup', 'FpGroup', 'SymmetricGroup', 
                     'AlternatingGroup', 'DihedralGroup', 'CyclicGroup', 'AbelianGroup'):
            return True
        if hasattr(obj, 'generators') and hasattr(obj, 'identity'):
            return True
        if obj in (sympy.QQ, sympy.RR, sympy.CC):
            return True
        return False

    def is_abelian(obj):
        if hasattr(obj, 'is_abelian'):
            return bool(obj.is_abelian)
        if obj in (sympy.QQ, sympy.RR, sympy.CC):
            return True
        return False

    def is_finitely_generated(obj):
        if hasattr(obj, 'is_finitely_generated'):
            return bool(obj.is_finitely_generated)
        tname = type(obj).__name__
        if tname in ('PermutationGroup', 'FpGroup', 'SymmetricGroup', 
                     'AlternatingGroup', 'DihedralGroup', 'CyclicGroup', 'AbelianGroup'):
            return True
        if tname == 'FreeGroup':
            try:
                return len(obj.generators) < float('inf')
            except Exception:
                return False
        if hasattr(obj, 'generators'):
            try:
                return len(list(obj.generators)) < float('inf')
            except Exception:
                pass
        if obj in (sympy.QQ, sympy.RR, sympy.CC):
            return False
        return False

    # H_1: G is an abelian group
    try:
        h1_ok = bool(is_group(G) and is_abelian(G))
    except Exception:
        h1_ok = False

    # H_2: G is finitely generated
    try:
        h2_ok = bool(is_finitely_generated(G))
    except Exception:
        h2_ok = False

    # ¬Q: H is NOT a finitely generated group
    try:
        q = bool(is_group(H) and is_finitely_generated(H))
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: G is finitely generated",
    "¬Q: H is not a finitely generated group"
]

N_HYP = 2
NEG_Q_INDEX = 2