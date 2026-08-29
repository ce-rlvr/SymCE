import sympy
import math

def conditions(witness):
    try:
        if len(witness) != 2:
            h1 = False
        else:
            m, n = witness
            h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > 0 and n > 0
    except Exception:
        h1 = False

    try:
        m, n = witness
        m_val = int(m)
        n_val = int(n)
        
        phi_mn = sympy.totient(m_val * n_val)
        phi_m = sympy.totient(m_val)
        phi_n = sympy.totient(n_val)
        
        part1 = phi_mn >= phi_m * phi_n
        
        eq_phi = (phi_mn == phi_m * phi_n)
        eq_gcd = (math.gcd(m_val, n_val) == 1)
        part2 = (eq_phi == eq_gcd)
        
        q = part1 and part2
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: It is not the case that (phi(mn) >= phi(m)phi(n) and (phi(mn) == phi(m)phi(n) iff gcd(m,n) == 1))"
]

N_HYP = 1
NEG_Q_INDEX = 1