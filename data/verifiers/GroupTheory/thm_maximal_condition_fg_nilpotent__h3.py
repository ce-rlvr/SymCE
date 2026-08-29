import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a nilpotent group
    try:
        if hasattr(G, 'is_nilpotent'):
            val = G.is_nilpotent
            h1 = bool(val() if callable(val) else val)
        elif G in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: G is finitely generated
    try:
        if hasattr(G, 'is_finitely_generated'):
            val = G.is_finitely_generated
            h2 = bool(val() if callable(val) else val)
        elif G in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h2 = False
        elif G == sympy.S.Integers:
            h2 = True
        elif hasattr(G, 'generators'):
            h2 = len(G.generators) < float('inf')
        elif isinstance(G, PermutationGroup):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: H is NOT finitely generated
    try:
        if hasattr(H, 'is_finitely_generated'):
            val = H.is_finitely_generated
            h_fg = bool(val() if callable(val) else val)
        elif H in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h_fg = False
        elif H == sympy.S.Integers:
            h_fg = True
        elif hasattr(H, 'generators'):
            h_fg = len(H.generators) < float('inf')
        elif isinstance(H, PermutationGroup):
            h_fg = True
        else:
            # If we cannot determine, assume it is finitely generated so ¬Q is False
            h_fg = True
    except Exception:
        h_fg = True

    neg_q = not h_fg

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: G is finitely generated",
    "¬Q: H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2