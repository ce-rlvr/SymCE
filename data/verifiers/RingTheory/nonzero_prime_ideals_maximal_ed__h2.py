import sympy
from sympy import ZZ, QQ, Symbol

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        R, P = witness
    except (TypeError, ValueError):
        R, P = sympy.ZZ, witness

    try:
        if R == sympy.ZZ or R == sympy.QQ:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            h1 = R.domain.is_Field
        elif hasattr(R, 'is_PID'):
            h1 = bool(R.is_PID)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if R == sympy.ZZ:
            is_max = (P != 0) and sympy.isprime(abs(int(P)))
        else:
            P_poly = sympy.sympify(P)
            if P_poly == 0:
                is_max = False
            else:
                factors = sympy.factor_list(P_poly)
                if len(factors[1]) == 1 and factors[1][0][1] == 1 and sympy.degree(factors[1][0][0]) > 0:
                    is_max = True
                else:
                    is_max = False
        neg_q = not is_max
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: P is not a maximal ideal in R"
]

N_HYP = 1
NEG_Q_INDEX = 1