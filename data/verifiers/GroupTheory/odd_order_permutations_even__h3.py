import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    sigma = None
    n = None
    
    try:
        # Witness can be either a tuple (n, sigma) or just sigma
        if isinstance(witness, tuple) and len(witness) == 2:
            n, sigma = witness
        else:
            sigma = witness
            if isinstance(sigma, Permutation):
                n = sigma.size
    except Exception:
        pass

    try:
        # H_1: n is a positive integer and sigma is an element of S_n
        h1 = isinstance(sigma, Permutation) and isinstance(n, int) and n > 0 and sigma.size <= n
    except Exception:
        h1 = False

    try:
        # H_2: the order of sigma is an odd integer
        h2 = isinstance(sigma, Permutation) and (sigma.order() % 2 == 1)
    except Exception:
        h2 = False

    try:
        # ¬Q: sigma is NOT an even permutation
        neg_q = isinstance(sigma, Permutation) and (not sigma.is_even)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer and sigma is an element of S_n",
    "H_2: the order of sigma is an odd integer",
    "¬Q: sigma is not an even permutation"
]

N_HYP = 2
NEG_Q_INDEX = 2