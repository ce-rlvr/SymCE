import sympy

class RingObj:
    def __init__(self, name, is_commutative, is_noetherian):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name

# Standard rings for witness construction
Z = RingObj("Z", True, True)
Q = RingObj("Q", True, True)
R_inf = RingObj("R[x1, x2, ...]", True, False)  # Commutative, but NOT Noetherian
M2 = RingObj("M2(R)", False, True)              # Noetherian, but NOT commutative

def is_comm(r):
    if hasattr(r, 'is_commutative'):
        return r.is_commutative
    if r in (sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC):
        return True
    return False

def is_noeth(r):
    if hasattr(r, 'is_noetherian'):
        return r.is_noetherian
    # Standard SymPy domains are Noetherian
    return True

def conditions(witness) -> list[bool]:
    try:
        # H_1: Let n be a positive integer (witness is a finite collection of length n >= 1)
        h1 = isinstance(witness, (list, tuple)) and len(witness) >= 1
    except Exception:
        h1 = False

    try:
        # H_2: Let R_1, R_2, ..., R_n be a finite collection of commutative rings
        h2 = all(is_comm(r) for r in witness)
    except Exception:
        h2 = False

    try:
        # ¬Q: The direct product ring R_1 x ... x R_n is NOT a Noetherian ring.
        # A finite direct product of rings is Noetherian if and only if EVERY factor is Noetherian.
        # Therefore, it is NOT Noetherian if AT LEAST ONE factor is NOT Noetherian.
        neg_q = any(not is_noeth(r) for r in witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer (witness is a non-empty finite collection)",
    "H_2: R_1, ..., R_n are commutative rings",
    "¬Q: The direct product ring is not Noetherian"
]

N_HYP = 2
NEG_Q_INDEX = 2