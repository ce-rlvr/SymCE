import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_faithfully_flat', False))
        elif hasattr(witness, 'is_faithfully_flat'):
            attr = witness.is_faithfully_flat
            h1 = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'f') and hasattr(witness.f, 'is_faithfully_flat'):
            attr = witness.f.is_faithfully_flat
            h1 = bool(attr() if callable(attr) else attr)
        elif isinstance(witness, tuple) and len(witness) == 3:
            _, _, f = witness
            if hasattr(f, 'is_faithfully_flat'):
                attr = f.is_faithfully_flat
                h1 = bool(attr() if callable(attr) else attr)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('S_is_noetherian', False))
        elif hasattr(witness, 'S_is_noetherian'):
            attr = witness.S_is_noetherian
            h2 = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'S') and hasattr(witness.S, 'is_noetherian'):
            attr = witness.S.is_noetherian
            h2 = bool(attr() if callable(attr) else attr)
        elif isinstance(witness, tuple) and len(witness) == 3:
            _, S, _ = witness
            if hasattr(S, 'is_noetherian'):
                attr = S.is_noetherian
                h2 = bool(attr() if callable(attr) else attr)
    except Exception:
        h2 = False

    try:
        r_noeth = True
        if isinstance(witness, dict):
            r_noeth = bool(witness.get('R_is_noetherian', True))
        elif hasattr(witness, 'R_is_noetherian'):
            attr = witness.R_is_noetherian
            r_noeth = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'R') and hasattr(witness.R, 'is_noetherian'):
            attr = witness.R.is_noetherian
            r_noeth = bool(attr() if callable(attr) else attr)
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, _, _ = witness
            if hasattr(R, 'is_noetherian'):
                attr = R.is_noetherian
                r_noeth = bool(attr() if callable(attr) else attr)
        neg_q = not r_noeth
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a faithfully flat ring homomorphism",
    "H_2: S is a Noetherian ring",
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2