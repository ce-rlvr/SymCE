import sympy
from sympy.ntheory import jacobi_symbol

# No specific named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        m, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        m_val = int(m)
        h1 = (m_val > 0) and (m_val % 2 == 1) and (m_val == m)
    except Exception:
        h1 = False

    try:
        n_val = int(n)
        h2 = (n_val > 0) and (n_val % 2 == 1) and (n_val == n)
    except Exception:
        h2 = False

    try:
        m_val = int(m)
        n_val = int(n)
        lhs = jacobi_symbol(m_val, n_val) * jacobi_symbol(n_val, m_val)
        rhs = (-1) ** (((m_val - 1) // 2) * ((n_val - 1) // 2))
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m is an odd positive integer",
    "H_2: n is an odd positive integer",
    "¬Q: (m/n)(n/m) != (-1)^(((m-1)/2)*((n-1)/2))"
]

N_HYP = 2
NEG_Q_INDEX = 2