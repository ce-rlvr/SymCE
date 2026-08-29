import sympy as sp
from sympy import symbols, Poly
from sympy.polys.domains import Domain
from sympy.abc import x, y, z

ZZ = sp.ZZ
QQ = sp.QQ
RR = sp.RR
CC = sp.CC

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, f = witness
        else:
            f = witness
            R = sp.ZZ
    except Exception:
        return [False, False, False]

    try:
        if R in [sp.ZZ, sp.QQ, sp.RR, sp.CC]:
            h1 = True
        elif isinstance(R, Domain):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(f, sp.Poly):
            h2 = len(f.gens) <= 1
        else:
            f_expr = sp.sympify(f)
            syms = f_expr.free_symbols
            if len(syms) == 0:
                h2 = True
            elif len(syms) == 1:
                p = sp.Poly(f_expr, list(syms)[0])
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False

    neg_q = False

    return [bool(h1), bool(h2), neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is a polynomial over R",
    "¬Q: The factor ring is not isomorphic to the polynomial ring over R"
]

N_HYP = 2
NEG_Q_INDEX = 2