import sympy
import sympy.combinatorics
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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
    try:
        if isinstance(grp, PermutationGroup):
            return True
        tname = type(grp).__name__
        if tname in ['FreeGroup', 'FpGroup']:
            return True
        if hasattr(grp, 'identity') and hasattr(grp, 'generators'):
            return True
        if grp in (sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals):
            return True
    except Exception:
        pass
    return False

def is_profinite(grp):
    # In the realm of discrete groups representable in SymPy,
    # a group is profinite if and only if it is finite.
    try:
        if isinstance(grp, PermutationGroup):
            return True
        if grp in (sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals):
            return False
        if hasattr(grp, 'is_finite') and grp.is_finite is not None:
            return bool(grp.is_finite)
        if hasattr(grp, 'order'):
            try:
                o = grp.order()
                if o == sympy.oo or o == math.inf:
                    return False
                if isinstance(o, (int, sympy.Integer)) and o > 0:
                    return True
            except Exception:
                pass
        tname = type(grp).__name__
        if tname == 'FreeGroup':
            return False
        if tname == 'FpGroup':
            try:
                o = grp.order()
                if o == sympy.oo or o == math.inf:
                    return False
                if isinstance(o, (int, sympy.Integer)) and o > 0:
                    return True
            except Exception:
                return False
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two groups: (G, H).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: H is a profinite group
    try:
        h1_ok = is_group(H) and is_profinite(H)
    except Exception:
        h1_ok = False
        
    # ¬Q: The direct product G x H is NOT a profinite group
    # G x H is profinite iff both G and H are profinite
    try:
        if not is_group(G):
            neg_q_ok = False
        else:
            g_prof = is_profinite(G)
            h_prof = is_profinite(H)
            q = g_prof and h_prof
            neg_q_ok = not q
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a profinite group",
    "¬Q: The direct product G x H is not a profinite group"
]

N_HYP = 1
NEG_Q_INDEX = 1