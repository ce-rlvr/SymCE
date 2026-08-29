import sympy
from sympy import symbols

x, y = symbols('x y')

def conditions(witness):
    try:
        p = sympy.poly(witness, x, y)
        char = getattr(p.domain, 'char', 0)
        h1 = bool(char != 2)
    except Exception:
        h1 = False

    try:
        p = sympy.poly(witness, x, y)
        h2 = bool(p.total_degree() <= 2)
    except Exception:
        h2 = False

    try:
        coeff, factors = sympy.factor_list(witness)
        num_non_constant_factors = 0
        for f, mult in factors:
            if sympy.poly(f, x, y).total_degree() > 0:
                num_non_constant_factors += mult
        neg_q = bool(num_non_constant_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2",
    "H_2: f is a polynomial of degree at most 2 in x and y",
    "not Q: f is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2