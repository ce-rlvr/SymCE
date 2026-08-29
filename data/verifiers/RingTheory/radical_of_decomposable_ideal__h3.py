import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math

# Top-level setup for potential witness expressions
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

def rad(n):
    """Computes the generator of the radical of the ideal (n) in Z."""
    if n == 0:
        return 0
    n = abs(n)
    if n == 1:
        return 1
    res = 1
    for p in factorint(n):
        res *= p
    return res

def intersection(ideals):
    """Computes the generator of the intersection of a list of ideals (a_i) in Z."""
    if not ideals:
        return 1
    res = ideals[0]
    for a in ideals[1:]:
        if res == 0 or a == 0:
            res = 0
        else:
            res = abs(res * a) // math.gcd(res, a)
    return res

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to be a tuple (I, Q_list) or a dict with these keys,
    representing the ideal I and the list of ideals Q_i in the ring of integers Z.
    """
    try:
        if isinstance(witness, dict):
            I = witness['I']
            Q_list = witness['Q_list']
        else:
            I, Q_list = witness
        I = int(I)
        Q_list = [int(q) for q in Q_list]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring with identity
    # We evaluate this in Z, which is always a commutative ring with identity.
    h1_ok = True
    
    # H_2: I is a proper ideal of R
    # In Z, an ideal (I) is proper if I != 1 and I != -1.
    try:
        h2_ok = abs(I) != 1
    except Exception:
        h2_ok = False
        
    # ¬Q: The radical √I is not equal to the intersection of the prime ideals √Q_i
    try:
        rad_I = rad(I)
        rad_Qs = [rad(q) for q in Q_list]
        rhs = intersection(rad_Qs)
        
        # The conclusion fails if the radical of I is NOT equal to the intersection
        neg_q_ok = (rad_I != rhs)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "¬Q: The radical √I is not equal to the intersection of the prime ideals √Q_i"
]

N_HYP = 2
NEG_Q_INDEX = 2