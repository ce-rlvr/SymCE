import sympy
from sympy.ntheory import factorint
from sympy.abc import x, y, z

Z = sympy.S.Integers
Q = sympy.S.Rationals
R = sympy.S.Reals

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (tuple, list)):
            val = witness[-1]
        else:
            val = witness
            
        if isinstance(val, sympy.Expr) and val.free_symbols:
            h1 = True
            sqf = sympy.sqf_list(val)
            is_sq_free = all(mult == 1 for factor, mult in sqf[1])
            neg_q = not is_sq_free
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, (tuple, list)):
            val = witness[-1]
        else:
            val = witness
        n = abs(int(val))
        h1 = True
        if n == 0 or n == 1:
            neg_q = False
        else:
            factors = factorint(n)
            is_sq_free = all(v == 1 for v in factors.values())
            neg_q = not is_sq_free
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The radical of P is not equal to P"
]

N_HYP = 1
NEG_Q_INDEX = 1