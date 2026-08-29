import sympy
from sympy import symbols, Rational, Integer, Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    Since there are no remaining hypotheses, we only check if the conclusion fails.
    The conclusion is that R is a right coherent ring.
    Thus, neg_Q is True if R is NOT a right coherent ring.
    """
    try:
        # SymPy does not have a built-in `is_coherent` property for rings.
        # We check for custom attributes or string representations of known non-coherent rings
        # (e.g., polynomial rings with infinitely many variables).
        is_coherent = True
        
        if hasattr(witness, 'is_right_coherent'):
            is_coherent = bool(witness.is_right_coherent)
        elif hasattr(witness, 'is_coherent'):
            is_coherent = bool(witness.is_coherent)
        elif isinstance(witness, str):
            s = witness.lower()
            if 'not coherent' in s or 'non-coherent' in s or 'noncoherent' in s:
                is_coherent = False
            elif 'infinit' in s or '...' in s:
                is_coherent = False
                
        neg_q = not is_coherent
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a right coherent ring"
]

N_HYP = 0
NEG_Q_INDEX = 0