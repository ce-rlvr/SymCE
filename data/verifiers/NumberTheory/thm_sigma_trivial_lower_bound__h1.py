import sympy
from sympy.ntheory import divisor_sigma
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: n >= 2",
    "¬Q: sigma(n) < n + 1 (or undefined for non-integers)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # H_1: n >= 2
    try:
        h1 = bool(witness >= 2)
    except Exception:
        h1 = False

    # ¬Q: sigma(n) < n + 1
    try:
        # Check if the witness is an integer.
        # If it is not an integer, the sum of divisors function is undefined,
        # meaning the conclusion sigma(n) >= n + 1 fails to hold.
        is_int = False
        if isinstance(witness, int):
            is_int = True
        elif hasattr(witness, 'is_integer'):
            if callable(witness.is_integer):
                is_int = witness.is_integer()
            else:
                is_int = bool(witness.is_integer)
        
        if is_int:
            val = int(witness)
            neg_q = bool(divisor_sigma(val) < val + 1)
        else:
            # For non-integers (e.g., 2.5), the conclusion fails, so its negation is True.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]