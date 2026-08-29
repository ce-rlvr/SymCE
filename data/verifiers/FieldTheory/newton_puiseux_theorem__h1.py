import sympy
from sympy import QQ, RR, CC, ZZ, Symbol, factor_list
from sympy.polys.domains import GF

x = Symbol('x')
t = Symbol('t')

def conditions(witness):
    try:
        char_val = None
        if hasattr(witness, 'characteristic'):
            char_val = witness.characteristic() if callable(witness.characteristic) else witness.characteristic
        elif hasattr(witness, 'char'):
            char_val = witness.char() if callable(witness.char) else witness.char
        h1 = (char_val == 0)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_Field'):
            h2 = bool(witness.is_Field)
        elif hasattr(witness, 'is_field'):
            h2 = bool(witness.is_field)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        is_alg_closed = True
        if witness == CC:
            is_alg_closed = True
        else:
            polys = [x**2 + 1, x**2 - 2, x**3 - 2, x**5 - x + 1]
            for p in polys:
                try:
                    coeff, factors = factor_list(p, domain=witness)
                    if any(f.as_poly(x).degree() >= 2 for f, mult in factors):
                        is_alg_closed = False
                        break
                except Exception:
                    pass
            if is_alg_closed:
                is_alg_closed = (witness == CC)
        neg_q = not is_alg_closed
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of K is zero",
    "H_2: K((t)) is the field of formal Laurent series over K",
    "¬Q: The algebraic closure of K((t)) is not isomorphic to the field of Puiseux series over K"
]

N_HYP = 2
NEG_Q_INDEX = 2