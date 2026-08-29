import sympy
from sympy.abc import x, y
import sympy.polys.domains as domains

QQ = domains.QQ
ZZ = domains.ZZ
GF = domains.GF
RR = domains.RR
CC = domains.CC
QQ_I = QQ.algebraic_field(sympy.I)

def conditions(witness):
    try:
        F, c = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    try:
        h2 = bool(F.characteristic != 2)
    except Exception:
        h2 = False

    try:
        c_sym = sympy.sympify(c)
        _ = F.from_sympy(c_sym)
        poly = x**2 + y**2 - c_sym
        factors = sympy.factor_list(poly, domain=F)
        neg_q = sum(mult for fac, mult in factors[1]) > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The characteristic of F is not equal to 2",
    "neg_Q: The polynomial x^2 + y^2 - c is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2