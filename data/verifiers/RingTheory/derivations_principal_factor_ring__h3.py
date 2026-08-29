import sympy as sp
from sympy import Poly
from sympy.abc import x, y, z, t

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f = witness[0]
        else:
            f = witness
        f = Poly(f)
        domain = f.domain
        if domain == sp.ZZ:
            domain = sp.QQ
        char = getattr(domain, 'characteristic', None)
        if char is None:
            if domain in [sp.QQ, sp.RR, sp.CC]:
                char = 0
        h1 = bool(domain.is_Field and char == 0)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple):
            f = witness[0]
        else:
            f = witness
        f = Poly(f)
        h2 = bool(len(f.free_symbols) == 1 and f.degree() >= 1)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, tuple) and len(witness) > 1:
            f = Poly(witness[0])
            R = witness[1]
            no_rep_roots = bool(f.gcd(f.diff()).degree() == 0)
            if R == f.domain or R == sp.QQ:
                der_zero = True
            elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
                der_zero = False
            else:
                der_zero = False
            neg_q = bool(der_zero != no_rep_roots)
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic zero",
    "H_2: f is a non-constant polynomial",
    "not Q: conclusion fails"
]

N_HYP = 2
NEG_Q_INDEX = 2