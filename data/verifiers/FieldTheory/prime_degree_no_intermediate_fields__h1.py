import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    H1 = False
    neg_Q = False
    
    try:
        # Case 1: Witness is a permutation group (Galois group)
        if hasattr(witness, 'degree') and hasattr(witness, 'order'):
            deg = witness.degree
            if callable(deg):
                deg = deg()
            order = witness.order
            if callable(order):
                order = order()
            
            H1 = sympy.isprime(deg)
            neg_Q = not sympy.isprime(order) and order > 1
            return [bool(H1), bool(neg_Q)]
    except Exception:
        pass

    try:
        # Case 2: Witness is a tuple of (degree, order)
        if isinstance(witness, tuple) and len(witness) == 2:
            deg, order = witness
            if isinstance(deg, int) and isinstance(order, int):
                H1 = sympy.isprime(deg)
                neg_Q = not sympy.isprime(order) and order > 1
                return [bool(H1), bool(neg_Q)]
    except Exception:
        pass

    try:
        # Case 3: Witness is an integer (degree)
        if isinstance(witness, int):
            H1 = sympy.isprime(witness)
            neg_Q = False
            return [bool(H1), bool(neg_Q)]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: The degree of K over F is a prime number",
    "¬Q: There exists a field E such that F is a proper subfield of E and E is a proper subfield of K"
]

N_HYP = 1
NEG_Q_INDEX = 1