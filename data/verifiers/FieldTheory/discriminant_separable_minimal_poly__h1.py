import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        m = witness
        if not isinstance(m, Poly):
            m = Poly(m, x)
        F = m.domain
        h1 = bool(m.is_irreducible and m.LC() == F.one and m.degree() >= 1)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, Poly):
            m = Poly(witness, x)
        else:
            m = witness
        m_diff = m.diff()
        g = m.gcd(m_diff)
        h2 = bool(g.degree() == 0)
    except Exception:
        h2 = False

    try:
        if not isinstance(witness, Poly):
            m = Poly(witness, x)
        else:
            m = witness
        Delta = m.discriminant()
        h3 = True
    except Exception:
        h3 = False

    try:
        if not isinstance(witness, Poly):
            m = Poly(witness, x)
        else:
            m = witness
        F = m.domain
        Delta = m.discriminant()
        Delta_F = F.from_sympy(Delta)
        neg_q = bool(Delta_F == F.zero)
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ['H_1: m is the minimal polynomial over F', 'H_2: alpha is a separable element over F', 'H_3: Delta is the discriminant of m', 'not Q: Delta is zero or not in F']

N_HYP = 3
NEG_Q_INDEX = 3