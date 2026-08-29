import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        R, p = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(R.is_PID)
    except Exception:
        h1 = False

    try:
        is_max = False
        if p == 0 or p == getattr(R, 'zero', 0):
            is_max = getattr(R, 'is_Field', False)
        else:
            if R == ZZ:
                is_unit = (abs(p) == 1)
                if not is_unit:
                    is_max = sympy.isprime(abs(p))
            else:
                try:
                    is_unit = R.is_unit(p)
                except Exception:
                    is_unit = False
                if not is_unit:
                    is_max = sympy.Poly(p, domain=R).is_irreducible
        neg_q = not is_max
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Principal Ideal Domain (PID)",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1