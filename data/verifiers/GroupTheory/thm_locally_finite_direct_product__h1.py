import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo

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

def is_locally_finite(grp):
    try:
        if getattr(grp, 'is_finite', False):
            return True
    except Exception:
        pass
    try:
        if grp.order() < oo:
            return True
    except Exception:
        pass
    try:
        if type(grp).__name__ == 'FreeGroup':
            return len(grp.generators) == 0
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If H is a locally finite group, then G x H is a locally finite group."
    
    The witness should provide both G and H, e.g., as a tuple (G, H) or a dict.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False]

    # H_1: H is a locally finite group
    try:
        h1 = bool(is_locally_finite(H))
    except Exception:
        h1 = False

    # ¬Q: G x H is NOT a locally finite group
    # A direct product G x H is locally finite iff BOTH G and H are locally finite.
    try:
        g_loc_fin = is_locally_finite(G)
        h_loc_fin = is_locally_finite(H)
        neg_q = not (g_loc_fin and h_loc_fin)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a locally finite group",
    "¬Q: G x H is not a locally finite group"
]

N_HYP = 1
NEG_Q_INDEX = 1
