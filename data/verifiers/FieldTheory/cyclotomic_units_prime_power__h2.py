import sympy
from sympy import isprime, cyclotomic_poly, Symbol, resultant
import math

# Top-level setup
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Given a witness (p, k, a), checks the hypotheses and the negated conclusion.
    Returns [H1, H2, H3, neg_Q]
    """
    try:
        p, k, a = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H2: zeta_{p^k} is a primitive p^k-th root of unity
    try:
        n = p**k
        h2 = bool(int(n) == n and n >= 1)
    except Exception:
        h2 = False
        
    # H3: a is an integer such that a and p are coprime
    try:
        h3 = bool(int(a) == a and math.gcd(int(a), int(p)) == 1)
    except Exception:
        h3 = False
        
    # Conclusion: The element is a unit in the ring of integers Z[zeta_{p^k}]
    try:
        n = int(p**k)
        if n == 1:
            q = False
        elif n < 1:
            q = False
        else:
            a_int = int(a)
            if n > 50:
                q = (math.gcd(a_int, int(p)) == 1)
            else:
                x = Symbol('x')
                poly = cyclotomic_poly(n, x)
                a_mod = a_int % n
                if a_mod == 0:
                    q = False
                else:
                    num_norm = resultant(poly, x**a_mod - 1)
                    den_norm = resultant(poly, x - 1)
                    if den_norm == 0:
                        q = False
                    else:
                        norm = num_norm / den_norm
                        q = (abs(norm) == 1)
    except Exception:
        q = False
        
    neg_q = not q
    
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    'H_1: p is a prime number',
    'H_2: zeta_{p^k} is a primitive root of unity',
    'H_3: a and p are coprime',
    'not Q: The element is NOT a unit'
]

N_HYP = 3
NEG_Q_INDEX = 3