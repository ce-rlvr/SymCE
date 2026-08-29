import math
import sympy

def is_integer(x):
    return isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (m, a, R) where R is a sequence of m integers [r_1, ..., r_m].
    """
    try:
        m, a, R = witness
    except Exception:
        return [False, False, False]
    
    # H_1: m is a positive integer (and R is a sequence of length m representing r_1...r_m)
    try:
        h1 = (is_integer(m) and int(m) > 0 and 
              isinstance(R, (list, tuple)) and len(R) == int(m) and 
              all(is_integer(r) for r in R))
    except Exception:
        h1 = False
        
    # H_2: a is an integer such that gcd(a, m) = 1
    try:
        h2 = is_integer(a) and math.gcd(int(a), int(m)) == 1
    except Exception:
        h2 = False
        
    # ¬Q: The set {ar_1, ..., ar_m} is NOT a complete residue system modulo m
    try:
        m_val = int(m)
        a_val = int(a)
        residues = set((a_val * int(r)) % m_val for r in R)
        is_crs = (residues == set(range(m_val)))
        neg_q = not is_crs
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a is an integer such that gcd(a, m) = 1",
    "¬Q: The set {ar_1, ..., ar_m} is not a complete residue system modulo m"
]

N_HYP = 2
NEG_Q_INDEX = 2