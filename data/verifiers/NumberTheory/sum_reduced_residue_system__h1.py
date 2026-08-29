import sympy
import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        m, R = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a reduced residue system modulo m
    try:
        h1 = False
        if isinstance(m, (int, sympy.Integer)) and m >= 1:
            m_int = int(m)
            R_list = list(R)
            if all(isinstance(r, (int, sympy.Integer)) for r in R_list):
                if len(R_list) == sympy.totient(m_int):
                    if all(math.gcd(int(r), m_int) == 1 for r in R_list):
                        mod_R = set(int(r) % m_int for r in R_list)
                        if len(mod_R) == len(R_list):
                            h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: sum(R) is not congruent to 0 modulo m
    try:
        neg_q = False
        if isinstance(m, (int, sympy.Integer)) and m >= 1:
            m_int = int(m)
            R_list = list(R)
            s = sum(int(r) for r in R_list)
            if (s % m_int) != 0:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced residue system modulo m",
    "¬Q: sum(R) is not congruent to 0 modulo m"
]

N_HYP = 1
NEG_Q_INDEX = 1