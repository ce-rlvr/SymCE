import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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
    "H_1: F_q is a finite field with q elements",
    "¬Q: (A is diagonalizable over F_q) is not equivalent to (A^q = A)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        q, A = witness
    except Exception:
        return [False, False]
        
    # H_1: F_q is a finite field with q elements
    try:
        q_val = int(q)
        if q_val < 2:
            h1 = False
        else:
            factors = factorint(q_val)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False
        
    # ¬Q: A is diagonalizable over F_q if and only if A^q = A (must fail)
    try:
        q_val = int(q)
        factors = factorint(q_val)
        p = list(factors.keys())[0]
        
        def mat_pow_mod(M, exp, mod):
            res = eye(M.shape[0])
            base = M % mod
            while exp > 0:
                if exp % 2 == 1:
                    res = (res * base) % mod
                base = (base * base) % mod
                exp //= 2
            return res
            
        # A matrix over F_p is diagonalizable over F_q iff its minimal polynomial divides x^q - x
        # This is equivalent to A^q == A mod p
        A_mod_p = A % p
        A_q_mod_p = mat_pow_mod(A, q_val, p)
        is_diag = bool(A_q_mod_p == A_mod_p)
        
        # Evaluate exact equality A^q = A (which fails if A is an integer matrix not restricted to F_q)
        A_q = A**q_val
        is_eq = bool(A_q == A)
        
        neg_q_ok = (is_diag != is_eq)
    except Exception:
        neg_q_ok = False
        
    return [h1, neg_q_ok]