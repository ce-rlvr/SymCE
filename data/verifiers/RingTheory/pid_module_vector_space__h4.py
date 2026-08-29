import sympy
from sympy.abc import x

# Top-level setup for RingTheory
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (R_type, M_inv, p), where:
      - R_type is a string or SymPy domain (e.g., "ZZ") representing the PID R.
      - M_inv is a list of integers representing the invariant factors of a finitely 
        generated module M over R (e.g., [0] for Z, [2] for Z/2Z).
      - p is an integer representing the prime element in R.
    """
    try:
        R_type, M_inv, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a principal ideal domain
    try:
        h1 = (R_type == "ZZ" or R_type == ZZ)
    except Exception:
        h1 = False
        
    # H_2: M is a module over R
    try:
        h2 = isinstance(M_inv, (list, tuple)) and all(isinstance(d, (int, sympy.Integer)) for d in M_inv)
    except Exception:
        h2 = False
        
    # H_3: p is a prime element in R
    try:
        h3 = sympy.isprime(abs(int(p)))
    except Exception:
        h3 = False
        
    # ¬Q: M is not a vector space over R/(p)
    # M is a vector space over R/(p) with the induced scalar multiplication 
    # if and only if p annihilates M (i.e., pM = 0).
    # This means p must be a multiple of every invariant factor d_i (and d_i != 0).
    # The negation is that for some invariant factor, d_i == 0 or p is not divisible by d_i.
    try:
        if not M_inv:
            # The zero module is trivially a vector space over R/(p)
            neg_q = False
        else:
            neg_q = any(d == 0 or int(p) % int(d) != 0 for d in M_inv)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a module over R",
    "H_3: p is a prime element in R",
    "¬Q: M is not a vector space over R/(p)"
]

N_HYP = 3
NEG_Q_INDEX = 3