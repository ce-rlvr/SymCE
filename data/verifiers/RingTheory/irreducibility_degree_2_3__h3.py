import sympy
from sympy import Poly
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            expr, dom = witness
            f = Poly(expr, domain=dom)
        elif isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness, domain='QQ')
    except Exception:
        f = None

    try:
        h1_ok = f is not None and f.domain.is_Field
    except Exception:
        h1_ok = False

    try:
        h2_ok = f is not None and isinstance(f, Poly) and len(f.gens) == 1
    except Exception:
        h2_ok = False

    try:
        if f is None:
            neg_q_ok = False
        else:
            if f.degree() <= 0:
                is_irred = False
            else:
                factors = f.factor_list()[1]
                is_irred = (len(factors) == 1 and factors[0][1] == 1)
            
            if f.is_zero:
                has_no_roots = False
            else:
                roots = f.ground_roots()
                has_no_roots = (len(roots) == 0)
                
            neg_q_ok = (is_irred != has_no_roots)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F",
    "¬Q: f(x) is irreducible over F is not equivalent to f(x) has no roots in F"
]

N_HYP = 2
NEG_Q_INDEX = 2