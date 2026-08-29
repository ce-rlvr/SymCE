import sympy
from sympy.ntheory import totient

# Top-level setup
# No named bindings needed for number theory

def conditions(witness) -> list[bool]:
    try:
        m, n = witness
    except Exception:
        return [False, False]
        
    try:
        m_int = int(m)
        n_int = int(n)
        h1 = (m == m_int) and (n == n_int) and (m_int > 0) and (n_int > 0)
    except Exception:
        h1 = False
        
    try:
        m_int = int(m)
        n_int = int(n)
        neg_q = bool(totient(m_int * n_int) != totient(m_int) * totient(n_int))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: phi(mn) != phi(m)phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1