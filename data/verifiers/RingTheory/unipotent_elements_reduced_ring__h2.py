import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.ntheory import factorint

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6

def is_squarefree(n):
    if n < 1:
        return False
    factors = factorint(n)
    return all(exp == 1 for exp in factors.values())

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, u) where R is a reduced ring and u is an element of R.
    If a single value is provided, R is implicitly assumed to be the ring of integers (ZZ).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, u = witness
        else:
            R = ZZ
            u = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a reduced ring
    try:
        is_reduced = False
        is_valid_u = False
        
        if R in (ZZ, QQ, RR, CC):
            is_reduced = True
            if hasattr(u, 'is_Matrix') and u.is_Matrix:
                is_valid_u = False
            elif isinstance(u, (int, float, complex)):
                is_valid_u = True
            elif hasattr(u, 'is_number') and u.is_number:
                is_valid_u = True
            else:
                is_valid_u = False
        elif isinstance(R, str) and R in ('ZZ', 'QQ', 'RR', 'CC', 'Z', 'Q', 'R', 'C'):
            is_reduced = True
            if hasattr(u, 'is_Matrix') and u.is_Matrix:
                is_valid_u = False
            elif isinstance(u, (int, float, complex)):
                is_valid_u = True
            elif hasattr(u, 'is_number') and u.is_number:
                is_valid_u = True
            else:
                is_valid_u = False
        elif isinstance(R, int) and R >= 2:
            # Z/nZ is reduced iff n is square-free
            is_reduced = is_squarefree(R)
            is_valid_u = isinstance(u, int) or (hasattr(u, 'is_integer') and u.is_integer)
        elif hasattr(R, 'is_domain') and R.is_domain:
            is_reduced = True
            is_valid_u = True
            
        h1_ok = bool(is_reduced and is_valid_u)
    except Exception:
        h1_ok = False
        
    # ¬Q: u is not equal to the identity element 1
    try:
        if isinstance(R, int) and R >= 2:
            neg_q_ok = (int(u) % R) != 1
        else:
            neg_q_ok = bool(u != 1)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "¬Q: u is not equal to the identity element 1"
]

N_HYP = 1
NEG_Q_INDEX = 1