import sympy
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 2",
    "H_2: f(x) is a monic polynomial over Z",
    "H_3: |a_{n-1}| > 1 + |a_{n-2}| + ... + |a_0|",
    "~Q: f(x) is not irreducible over the rational numbers Q"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # H1: n >= 2
    try:
        p = sympy.Poly(witness, x)
        n = p.degree()
        h1 = bool(n >= 2)
    except Exception:
        h1 = False

    # H2: monic polynomial over Z
    try:
        p = sympy.Poly(witness, x)
        is_ZZ = (p.domain == sympy.ZZ)
        is_monic = (p.LC() == 1)
        h2 = bool(is_ZZ and is_monic)
    except Exception:
        h2 = False

    # H3: |a_{n-1}| > 1 + |a_{n-2}| + ... + |a_0|
    try:
        p = sympy.Poly(witness, x)
        n = p.degree()
        coeffs = p.all_coeffs()
        if n >= 2 and len(coeffs) == n + 1:
            abs_a_n_minus_1 = abs(coeffs[1])
            sum_abs_others = sum(abs(c) for c in coeffs[2:])
            h3 = bool(abs_a_n_minus_1 > 1 + sum_abs_others)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: f(x) is not irreducible over Q
    try:
        _, factors = sympy.factor_list(witness, domain='QQ')
        num_factors = sum(m for f, m in factors if sympy.degree(f, x) > 0)
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]