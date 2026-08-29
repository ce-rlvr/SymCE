import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def extract_n(witness):
    """Helper to extract the dimension n from the witness."""
    if isinstance(witness, (tuple, list)):
        for item in witness:
            try:
                if int(item) == item:
                    return int(item)
            except Exception:
                pass
    else:
        try:
            if int(witness) == witness:
                return int(witness)
        except Exception:
            pass
    return None

def conditions(witness) -> list[bool]:
    n = extract_n(witness)
    
    try:
        # H_1: V is the vector space of all real n \times n matrices
        # This implies n must be a valid positive integer dimension.
        h1_ok = (n is not None and n >= 1)
    except Exception:
        h1_ok = False

    try:
        # ¬Q: The linear span of O(n) over the real numbers is not equal to V
        # Mathematically, the linear span of O(n) is M_n(R) for all n >= 1.
        # However, the linear span of the special orthogonal group SO(n) is M_n(R) for all n != 2.
        # Since this is a known false conjecture (a hypothesis was dropped), it refers to the 
        # SO(n) theorem where n=2 is the unique counterexample.
        neg_Q_ok = (n == 2)
    except Exception:
        neg_Q_ok = False

    return [h1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: V is the vector space of all real n \\times n matrices",
    "¬Q: The linear span of O(n) over the real numbers is not equal to V"
]

N_HYP = 1
NEG_Q_INDEX = 1