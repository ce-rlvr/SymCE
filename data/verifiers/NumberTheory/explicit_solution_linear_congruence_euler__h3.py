import sympy
from sympy.ntheory import totient

def conditions(witness) -> list[bool]:
    try:
        a, b, m = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(b, (int, sympy.Integer)) and \
             isinstance(m, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        h2 = h1 and int(m) > 0
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            a_int = int(a)
            b_int = int(b)
            m_int = int(m)
            phi_m = int(totient(m_int))
            
            # The proposed solution is x = a^{\phi(m)-1}b.
            # We check if ax \equiv b \pmod m.
            # ax = a * a^{\phi(m)-1}b = a^{\phi(m)}b.
            # We compute this modulo m to avoid large integers.
            lhs = (pow(a_int, phi_m, m_int) * b_int) % m_int
            rhs = b_int % m_int
            
            # neg_Q is True if it is NOT a solution
            neg_q = (lhs != rhs)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, m are integers",
    "H_2: m > 0",
    "¬Q: x = a^{\\phi(m)-1}b is not a solution to ax \\equiv b \\pmod m"
]

N_HYP = 2
NEG_Q_INDEX = 2