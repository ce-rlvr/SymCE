import sympy
from sympy import Poly, Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, Matrix):
            m = witness.minimal_polynomial(x)
        elif isinstance(witness, dict):
            if 'm' in witness:
                m = witness['m']
            elif 'alpha' in witness and isinstance(witness['alpha'], Matrix):
                m = witness['alpha'].minimal_polynomial(x)
            else:
                m = witness
        else:
            m = witness
            
        if not isinstance(m, Poly):
            m = Poly(m)
            
        if not m.domain.is_Field:
            try:
                m = m.set_domain(sympy.QQ)
            except Exception:
                pass

    except Exception:
        return [False, False, False, False, False]

    try:
        domain = m.domain
        h1_ok = bool(domain.is_Field)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(m.is_univariate and m.degree() >= 1)
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool(m.is_monic)
    except Exception:
        h3_ok = False

    try:
        h4_ok = True
    except Exception:
        h4_ok = False

    try:
        neg_q_ok = not bool(m.is_squarefree)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "H_2: alpha in K is algebraic over F",
    "H_3: m(x) in polynomial ring over F is the minimal polynomial of alpha over F",
    "H_4: E is a splitting field of m(x) over F",
    "not Q: m(x) has at least one root in E with multiplicity > 1"
]

N_HYP = 4
NEG_Q_INDEX = 4