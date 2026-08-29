import sympy
from sympy import cyclotomic_poly, Poly, Rational
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: Phi_n(x) is the n-th cyclotomic polynomial",
    "¬Q: Phi_n(x) does not belong to the polynomial ring over Z"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_cyclotomic_poly(n, var):
    if isinstance(n, (int, sympy.Integer)):
        return cyclotomic_poly(int(n), var)
    elif isinstance(n, Rational):
        p, q = n.p, n.q
        return cyclotomic_poly(p, var**(Rational(1, q)))
    elif isinstance(n, float):
        from fractions import Fraction
        f = Fraction(n).limit_denominator()
        return cyclotomic_poly(f.numerator, var**(Rational(1, f.denominator)))
    else:
        return cyclotomic_poly(int(n), var)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, P = witness
        else:
            n = witness
            P = get_cyclotomic_poly(n, x)
    except Exception:
        return [False, False]
    
    try:
        if isinstance(P, Poly):
            try:
                expected = Poly(get_cyclotomic_poly(n, x), x, domain=P.domain)
                h1_ok = (P == expected)
            except Exception:
                h1_ok = False
        else:
            expected = get_cyclotomic_poly(n, x)
            h1_ok = (sympy.simplify(P - expected) == 0)
    except Exception:
        h1_ok = False

    try:
        if isinstance(P, Poly):
            if P.domain.is_ZZ:
                q = True
            elif P.domain.is_QQ:
                q = all(c.is_integer for c in P.coeffs())
            else:
                q = False
        else:
            try:
                P_simp = sympy.simplify(P)
                poly_P = Poly(P_simp, x)
                if poly_P.domain.is_ZZ:
                    q = True
                elif poly_P.domain.is_QQ:
                    q = all(c.is_integer for c in poly_P.coeffs())
                elif poly_P.domain.is_RR or poly_P.domain.is_CC:
                    q = all(c.is_integer for c in poly_P.coeffs())
                else:
                    q = all(sympy.simplify(c).is_integer for c in poly_P.coeffs())
            except Exception:
                q = False
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]