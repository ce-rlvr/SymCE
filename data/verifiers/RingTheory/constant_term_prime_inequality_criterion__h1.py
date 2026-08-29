import sympy
from sympy import abc
from sympy import Poly

# Top-level setup
x = abc.x

def conditions(witness):
    try:
        poly = Poly(witness, x)
        coeffs = poly.all_coeffs()
        if len(coeffs) < 2:
            a0 = coeffs[0] if coeffs else sympy.S.Zero
            other_coeffs = []
        else:
            a0 = coeffs[-1]
            other_coeffs = coeffs[:-1]
    except Exception:
        return [False, False, False]

    # H_1: The constant term a_0 is equal to a prime number p
    try:
        if a0.is_Rational and a0.q == 1:
            p = int(a0.p)
            h1 = sympy.isprime(p)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: p > sum_{i=1}^n |a_i|
    try:
        if h1:
            sum_abs = sum(abs(c) for c in other_coeffs)
            h2 = bool(p > sum_abs)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The polynomial f(x) is NOT irreducible over QQ
    try:
        if poly.degree() < 1:
            # Constants are units in QQ[x], hence not irreducible
            neg_q = True
        else:
            if not all(c.is_Rational for c in coeffs):
                neg_q = False
            else:
                _, factors = sympy.factor_list(witness, domain='QQ')
                # A polynomial is irreducible if it has exactly one prime factor with multiplicity 1
                is_irred = (len(factors) == 1) and (factors[0][1] == 1)
                neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The constant term a_0 is equal to a prime number p",
    "H_2: p > sum_{i=1}^n |a_i|",
    "¬Q: The polynomial f(x) is reducible over QQ"
]

N_HYP = 2
NEG_Q_INDEX = 2