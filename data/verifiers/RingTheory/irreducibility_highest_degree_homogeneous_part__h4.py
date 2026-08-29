import sympy
from sympy import symbols, Poly

x, y = symbols('x y')

def conditions(witness):
    try:
        p = Poly(witness, x, y, domain='QQ')
        h1 = True
    except Exception:
        h1 = False

    try:
        p = Poly(witness, x, y, domain='QQ')
        h2 = p.total_degree() >= 1
    except Exception:
        h2 = False

    try:
        p = Poly(witness, x, y, domain='QQ')
        # Every polynomial can be uniquely written as a sum of its homogeneous components
        h3 = True
    except Exception:
        h3 = False

    try:
        p = Poly(witness, x, y, domain='QQ')
        const, factors = p.factor_list()
        num_non_constant_factors = sum(power for fac, power in factors if fac.total_degree() >= 1)
        neg_q = num_non_constant_factors > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a polynomial of degree n >= 1",
    "H_3: f is a sum of homogeneous polynomials",
    "¬Q: f is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3