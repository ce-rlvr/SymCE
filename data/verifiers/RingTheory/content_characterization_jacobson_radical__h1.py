import sympy
from sympy import Poly

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        H1 = False
        if isinstance(witness, Poly):
            H1 = True
        elif hasattr(witness, 'is_poly') and witness.is_poly:
            H1 = True
    except Exception:
        H1 = False

    try:
        neg_Q = False
        if hasattr(witness, 'in_Jacobson_radical') and hasattr(witness, 'content_ideal_in_nilradical'):
            f_in_J = bool(witness.in_Jacobson_radical())
            c_in_Nil = bool(witness.content_ideal_in_nilradical())
            neg_Q = (f_in_J != c_in_Nil)
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: f is a polynomial in R(x)",
    "¬Q: f in J(R(x)) is not equivalent to c(f) in nilradical"
]

N_HYP = 1
NEG_Q_INDEX = 1