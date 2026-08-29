import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p does not divide a",
    "¬Q: a^{p-1} is not congruent to 1 mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        a, p = witness
    except Exception:
        return [False, False, False]
    
    # H1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # H2: p does not divide a
    try:
        res = a % p
        if hasattr(res, 'is_Matrix') and res.is_Matrix:
            h2 = not bool(res.is_zero_matrix)
        else:
            h2 = bool(res != 0)
    except Exception:
        h2 = False
        
    # neg_Q: a^{p-1} \not\equiv 1 \pmod p
    try:
        try:
            # Try standard 3-argument pow for efficiency with integers
            val = pow(a, p - 1, p)
            neg_q = bool(val != 1)
        except Exception:
            # Fallback for floats, matrices, etc.
            val = (a ** (p - 1)) % p
            if hasattr(val, 'is_Matrix') and val.is_Matrix:
                neg_q = bool(val != eye(val.rows))
            else:
                neg_q = bool(val != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]