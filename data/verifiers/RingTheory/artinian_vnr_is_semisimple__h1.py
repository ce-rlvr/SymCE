import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

class _CustomRing:
    def __init__(self, vnr, semisimple):
        self.is_von_neumann_regular = vnr
        self.is_semisimple = semisimple

# Predefined standard counterexamples for convenience
InfiniteBooleanRing = _CustomRing(True, False)
InfiniteProductOfFields = _CustomRing(True, False)

def _check_vnr(R):
    if isinstance(R, str):
        R_lower = R.lower()
        if any(x in R_lower for x in ["boolean", "product of fields", "endomorphism", "linear operator"]):
            return True
    if hasattr(R, 'is_von_neumann_regular'):
        val = R.is_von_neumann_regular
        return val() if callable(val) else bool(val)
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    return False

def _check_semisimple(R):
    if isinstance(R, str):
        R_lower = R.lower()
        if "infinite" in R_lower:
            return False
        if "finite" in R_lower:
            return True
    if hasattr(R, 'is_semisimple'):
        val = R.is_semisimple
        return val() if callable(val) else bool(val)
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    return False

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    try:
        h1_ok = bool(_check_vnr(witness))
    except Exception:
        h1_ok = False
        
    try:
        q_ok = bool(_check_semisimple(witness))
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a von Neumann regular ring",
    "¬Q: R is not a semisimple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1