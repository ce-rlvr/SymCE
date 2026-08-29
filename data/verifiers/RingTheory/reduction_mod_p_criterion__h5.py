import sympy
from sympy import Poly, factor_list
from sympy.ntheory import isprime
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                p, f = witness
                D = ZZ
            elif len(witness) == 3:
                D, p, f = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    try:
        is_ZZ = (D == ZZ or str(D) == 'ZZ')
        is_QQ = (D == QQ or str(D) == 'QQ')
        h1 = is_ZZ or is_QQ
    except Exception:
        h1 = False

    try:
        if is_ZZ:
            h2 = isprime(abs(int(p))) or int(p) == 0
        elif is_QQ:
            h2 = (int(p) == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        poly_f = Poly(f, x, domain=ZZ if is_ZZ else QQ)
        h3 = poly_f.degree() >= 1
    except Exception:
        h3 = False

    try:
        poly_f = Poly(f, x, domain=ZZ if is_ZZ else QQ)
        an = poly_f.LC()
        if is_ZZ:
            if int(p) == 0:
                h4 = (an != 0)
            else:
                h4 = (an % int(p) != 0)
        elif is_QQ:
            h4 = (an != 0)
        else:
            h4 = False
    except Exception:
        h4 = False

    try:
        factors = factor_list(f, domain=ZZ if is_ZZ else QQ)
        pos_deg_factors_count = sum(mult for fac, mult in factors[1] if Poly(fac, x).degree() >= 1)
        neg_q = pos_deg_factors_count >= 2
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: D is a unique factorization domain",
    "H_2: P is a prime ideal of D",
    "H_3: f(x) is a non-constant polynomial over D",
    "H_4: The leading coefficient a_n is not an element of P",
    "¬Q: f(x) can be factored into two polynomials of positive degree over D"
]

N_HYP = 4
NEG_Q_INDEX = 4