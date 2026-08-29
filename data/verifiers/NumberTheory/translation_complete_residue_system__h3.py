import sympy
from sympy import Integer

def is_crs(A, m):
    if not isinstance(A, (set, list, tuple)):
        return False
    if len(A) != m:
        return False
    for a in A:
        if not isinstance(a, (int, Integer)):
            return False
    try:
        residues = set(int(a) % int(m) for a in A)
        return len(residues) == m
    except Exception:
        return False

def conditions(witness):
    try:
        m, S, c = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(m, (int, Integer)) and m > 0
    except Exception:
        h1 = False
        
    try:
        h2 = is_crs(S, m)
    except Exception:
        h2 = False
        
    try:
        T = [x + c for x in S]
        neg_q = not is_crs(T, m)
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: S is a complete residue system modulo m",
    "¬Q: The set {x + c | x in S} is not a complete residue system modulo m"
]

N_HYP = 2
NEG_Q_INDEX = 2