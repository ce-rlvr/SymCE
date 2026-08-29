import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def is_prime_power(n):
    if not isinstance(n, int) or n < 2:
        return False
    factors = sympy.factorint(n)
    return len(factors) == 1

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (F_val, n), where F_val represents 
    the finite field (or its order q) and n is the integer dimension.
    """
    try:
        F_val, n = witness
        if hasattr(F_val, 'order'):
            q = int(F_val.order)
        elif hasattr(F_val, 'mod'):
            q = int(F_val.mod)
        else:
            q = int(F_val)
    except Exception:
        return [False, False, False]
    
    # H_1: F is a finite field of order q
    try:
        h1_ok = is_prime_power(q)
    except Exception:
        h1_ok = False
        
    # H_2: n is an integer strictly greater than 1
    try:
        h2_ok = isinstance(n, int) and n > 1
    except Exception:
        h2_ok = False
        
    # ¬Q: The number of elements in SL(n, F) is NOT q^{n(n-1)/2} \prod_{i=2}^n (q^i - 1)
    try:
        # The true mathematical order of SL(n, F) for a finite field of order q
        true_order = (q**(n*(n-1)//2)) * math.prod(q**i - 1 for i in range(2, n+1))
        
        # The formula given in the conclusion of the conjecture
        formula = (q**(n*(n-1)//2)) * math.prod(q**i - 1 for i in range(2, n+1))
        
        neg_q_ok = true_order != formula
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: n is an integer strictly greater than 1",
    "¬Q: The number of elements in SL(n, F) is not q^{n(n-1)/2} \\prod_{i=2}^n (q^i - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2