import sympy
import sympy.ntheory
from sympy.abc import x

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and int(witness) >= 1
    except Exception:
        h1 = False

    try:
        h2 = isinstance(witness, (int, sympy.Integer)) and int(witness) >= 1
    except Exception:
        h2 = False

    try:
        if not (isinstance(witness, (int, sympy.Integer)) and int(witness) >= 1):
            neg_q = False
        else:
            n = int(witness)
            phi_n = sympy.ntheory.totient(n)
            poly_x = sympy.cyclotomic_poly(n, x)
            poly_1_x = sympy.cyclotomic_poly(n, 1/x)
            lhs = (x**phi_n) * poly_1_x
            rhs = poly_x
            
            diff = sympy.expand(lhs - rhs)
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Phi_n(x) is the n-th cyclotomic polynomial",
    "H_2: phi(n) is Euler's totient function evaluated at n",
    "¬Q: x^phi(n) * Phi_n(1/x) != Phi_n(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2