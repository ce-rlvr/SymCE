import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that n must be a positive integer.
    For negative integers, Euler's totient function phi(n) is undefined (or defined as phi(|n|)),
    and the standard formulation of the theorem fails.
    """
    try:
        # H_1: n must be a non-zero integer for a primitive n-th root of unity to exist.
        is_int = isinstance(witness, int) and not isinstance(witness, bool)
        is_sympy_int = isinstance(witness, sympy.Integer)
        h1 = bool((is_int or is_sympy_int) and witness != 0)
    except Exception:
        h1 = False
        
    try:
        # H_2: Q(zeta_n) is well-defined as long as zeta_n is well-defined.
        h2 = h1
    except Exception:
        h2 = False
        
    try:
        # ¬Q: The conclusion fails if n < 0 because phi(n) is undefined for negative integers,
        # meaning the degree cannot strictly be phi(n) as stated.
        neg_q = bool(witness < 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity in the complex numbers (n is a non-zero integer)",
    "H_2: Q(zeta_n) is the n-th cyclotomic extension of the rational numbers Q",
    "¬Q: The extension Q(zeta_n)/Q is NOT a Galois extension of degree phi(n) or its Galois group is NOT isomorphic to (Z/nZ)^times"
]

N_HYP = 2
NEG_Q_INDEX = 2