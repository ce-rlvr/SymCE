import sympy
from sympy.ntheory import isprime
from sympy import eye, zeros

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_eq_mod(A, B, p):
    """Helper to check if A == B mod p, handling both scalars and matrices."""
    try:
        if hasattr(A, 'shape') and isinstance(B, (int, sympy.Integer)):
            if B == 0:
                diff = A
            elif B == 1:
                if A.shape[0] != A.shape[1]:
                    return False
                diff = A - sympy.eye(A.shape[0])
            else:
                if A.shape[0] != A.shape[1]:
                    return False
                diff = A - B * sympy.eye(A.shape[0])
        else:
            diff = A - B
            
        if hasattr(diff, '__iter__'):
            return all(sympy.S(val) % p == 0 for val in diff)
        else:
            return sympy.S(diff) % p == 0
    except Exception:
        return False

def conditions(witness):
    try:
        x, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: x^2 \equiv x \pmod p
    try:
        h2 = bool(is_eq_mod(x**2, x, p))
    except Exception:
        h2 = False
        
    # ¬Q: x \not\equiv 0 \pmod p and x \not\equiv 1 \pmod p
    try:
        neg_q = (not is_eq_mod(x, 0, p)) and (not is_eq_mod(x, 1, p))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: x^2 \\equiv x \\pmod p",
    "¬Q: x \\not\\equiv 0 \\pmod p and x \\not\\equiv 1 \\pmod p"
]

N_HYP = 2
NEG_Q_INDEX = 2