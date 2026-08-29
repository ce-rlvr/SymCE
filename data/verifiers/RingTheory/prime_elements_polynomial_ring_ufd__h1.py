import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = True
    neg_q = False
    
    try:
        if hasattr(witness, 'is_prime_in_R'):
            h1 = bool(witness.is_prime_in_R())
        elif hasattr(witness, 'p_is_prime_in_R'):
            h1 = bool(witness.p_is_prime_in_R())
        elif hasattr(witness, 'H1'):
            h1 = bool(witness.H1())
        elif isinstance(witness, tuple) and hasattr(witness[0], 'is_prime'):
            h1 = bool(witness[0].is_prime(witness[1]))
        elif isinstance(witness, dict) and 'H1' in witness:
            h1 = bool(witness['H1'])
    except Exception:
        h1 = False
        
    try:
        if hasattr(witness, 'is_polynomial_ring'):
            h2 = bool(witness.is_polynomial_ring())
        elif hasattr(witness, 'H2'):
            h2 = bool(witness.H2())
        elif isinstance(witness, dict) and 'H2' in witness:
            h2 = bool(witness['H2'])
    except Exception:
        h2 = True
        
    try:
        if hasattr(witness, 'is_prime_in_Rx'):
            neg_q = not bool(witness.is_prime_in_Rx())
        elif hasattr(witness, 'p_is_prime_in_Rx'):
            neg_q = not bool(witness.p_is_prime_in_Rx())
        elif hasattr(witness, 'Q'):
            neg_q = not bool(witness.Q())
        elif isinstance(witness, tuple) and hasattr(witness[0], 'is_prime_in_poly_ring'):
            neg_q = not bool(witness[0].is_prime_in_poly_ring(witness[1]))
        elif isinstance(witness, dict) and 'Q' in witness:
            neg_q = not bool(witness['Q'])
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime element of R",
    "H_2: R_x is the polynomial ring over R",
    "not Q: The element p is not a prime element in the ring R_x"
]

N_HYP = 2
NEG_Q_INDEX = 2