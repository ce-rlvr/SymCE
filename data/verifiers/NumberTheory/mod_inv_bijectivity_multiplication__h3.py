import sympy
from sympy import Integer

def conditions(witness) -> list[bool]:
    try:
        m, a, S = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: m is a positive integer
    try:
        h1 = isinstance(m, (int, Integer)) and m > 0
    except Exception:
        h1 = False
        
    # H_2: a is an integer
    try:
        h2 = isinstance(a, (int, Integer))
    except Exception:
        h2 = False
        
    # H_3: S is a complete residue system modulo m
    try:
        S_list = list(S)
        if h1:
            all_ints = all(isinstance(x, (int, Integer)) for x in S_list)
            residues = {int(x) % int(m) for x in S_list}
            h3 = all_ints and (len(residues) == int(m)) and (len(S_list) == int(m))
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: The set {a * x (mod m) | x ∈ S} is not a complete residue system modulo m
    try:
        if h1 and h2:
            S_list = list(S)
            new_residues = {(int(a) * int(x)) % int(m) for x in S_list}
            neg_q = len(new_residues) < int(m)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a is an integer",
    "H_3: S is a complete residue system modulo m",
    "¬Q: The set {a * x (mod m) | x in S} is not a complete residue system modulo m"
]

N_HYP = 3
NEG_Q_INDEX = 3