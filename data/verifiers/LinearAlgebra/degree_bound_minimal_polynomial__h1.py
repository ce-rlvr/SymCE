import sympy
from sympy import Matrix, eye, zeros, degree, expand
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness can be (A, m_A, n) or just (A, n) where m_A is implicit
        if len(witness) == 3:
            A, m_A, n = witness
        elif len(witness) == 2:
            A, n = witness
            m_A = A.minpoly(x)
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: m_A(x) is the minimal polynomial of A
    try:
        min_poly = A.minpoly(x)
        h1_ok = bool(expand(m_A - min_poly) == 0)
    except Exception:
        h1_ok = False

    # ¬Q: The degree of m_A(x) is strictly greater than n
    try:
        deg = degree(m_A, x)
        neg_q_ok = bool(deg > n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: m_A(x) is the minimal polynomial of A",
    "¬Q: The degree of m_A(x) is strictly greater than n"
]

N_HYP = 1
NEG_Q_INDEX = 1