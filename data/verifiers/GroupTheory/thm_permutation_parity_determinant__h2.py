import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Matrix, eye, zeros

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

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The missing hypothesis is the definition of P_sigma as the permutation matrix of sigma.
    Thus, P_sigma is a free variable and the witness must provide both sigma and P_sigma.
    """
    # Check H_1: sigma is a permutation in the symmetric group S_n
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            h1 = False
        else:
            sigma, P_sigma = witness
            h1 = isinstance(sigma, Permutation)
    except Exception:
        h1 = False

    # Check ¬Q: The sign of the permutation sigma is NOT equal to the determinant of the matrix P_sigma
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            neg_q = False
        else:
            sigma, P_sigma = witness
            sign_sigma = sigma.signature()
            
            if not hasattr(P_sigma, 'det'):
                P_sigma = Matrix(P_sigma)
                
            det_P = P_sigma.det()
            neg_q = bool(sign_sigma != det_P)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation in the symmetric group S_n",
    "¬Q: The sign of the permutation sigma is not equal to the determinant of the matrix P_sigma"
]

N_HYP = 1
NEG_Q_INDEX = 1