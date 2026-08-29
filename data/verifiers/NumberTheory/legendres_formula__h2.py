import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math

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

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The highest exponent v such that p^v divides n! is not exactly the sum"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        n, p = witness
    except Exception:
        return [False, False]
    
    # H_1: n is a positive integer
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and not isinstance(n, bool) and n > 0
    except Exception:
        h1 = False

    # ¬Q: The highest exponent v such that p^v divides n! is not exactly the sum
    try:
        if not (isinstance(p, int) or isinstance(p, sympy.Integer)) or isinstance(p, bool):
            neg_q = False
        else:
            p = int(p)
            n_int = int(n)
            if p in (0, 1, -1):
                # For p in {0, 1, -1}, the standard formula is undefined or infinite,
                # we conservatively return False to avoid dealing with infinities.
                neg_q = False
            else:
                # Calculate the highest exponent v such that p^v divides n!
                factors = factorint(abs(p))
                v = float('inf')
                for prime, a in factors.items():
                    v_prime = 0
                    k = 1
                    while prime**k <= n_int:
                        v_prime += n_int // (prime**k)
                        k += 1
                    v_p = v_prime // a
                    if v_p < v:
                        v = v_p
                if v == float('inf'):
                    v = 0
                
                # Calculate the sum \sum_{k=1}^{\infty} \lfloor n / p^k \rfloor
                if p >= 2:
                    s = 0
                    k = 1
                    while p**k <= n_int:
                        s += n_int // (p**k)
                        k += 1
                    neg_q = (v != s)
                else:
                    # For p <= -2, the sum diverges and thus does not equal the finite integer v
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]