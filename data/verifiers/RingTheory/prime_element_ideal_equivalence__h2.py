import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    try:
        if isinstance(witness, (tuple, list)):
            p = witness[-1]
        else:
            p = witness
        p = int(p)
        # We evaluate the conditions assuming the ring is Z, which is an integral domain.
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, (tuple, list)):
            p = witness[-1]
        else:
            p = witness
        p = int(p)
        
        # In Z, prime elements are non-zero, non-units that are prime numbers
        is_prime_element = (p != 0) and (abs(p) != 1) and sympy.isprime(abs(p))
        
        # In Z, prime ideals are (0) and (p) where p is a prime number
        is_prime_ideal = (p == 0) or (abs(p) != 1 and sympy.isprime(abs(p)))
        
        equivalence = (is_prime_element == is_prime_ideal)
        neg_q = not equivalence
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The equivalence between p being a prime element and (p) being a prime ideal fails"
]

N_HYP = 1
NEG_Q_INDEX = 1