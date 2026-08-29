import sympy
import sympy.ntheory
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def check_perfect(n):
    """Check if n is a perfect number."""
    if hasattr(sympy.ntheory, 'is_perfect'):
        return sympy.ntheory.is_perfect(n)
    else:
        if n <= 0:
            return False
        divs = sympy.ntheory.divisors(n)
        return sum(divs[:-1]) == n

def check_Q(n):
    """Check if n = 2^{p-1}(2^p - 1) for some prime p such that 2^p - 1 is prime."""
    if n <= 0:
        return False
    # p can be at most n.bit_length() + 1
    for p in range(2, n.bit_length() + 2):
        if (1 << (p - 1)) * ((1 << p) - 1) == n:
            if sympy.isprime(p) and sympy.isprime((1 << p) - 1):
                return True
    return False

def conditions(witness):
    try:
        # Ensure the witness is mathematically an integer
        if hasattr(witness, 'is_integer') and witness.is_integer is False:
            return [False]
        n = int(witness)
        if n != witness:
            return [False]
    except Exception:
        return [False]
    
    try:
        is_P = bool(check_perfect(n))
    except Exception:
        is_P = False
        
    try:
        is_Q = bool(check_Q(n))
    except Exception:
        is_Q = False
        
    # The conjecture states P(n) <-> Q(n).
    # The conclusion fails if P(n) is True and Q(n) is False, or vice versa (XOR).
    neg_q = (is_P != is_Q)
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: n is a perfect number XOR n is of the form 2^{p-1}(2^p - 1) with p and 2^p-1 prime"
]
N_HYP = 0
NEG_Q_INDEX = 0