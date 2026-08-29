import sympy
from sympy import factor_list
from sympy.ntheory import isprime
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        p = sympy.sympify(witness)
        if not p.is_integer:
            h1 = False
        else:
            h1 = bool(isprime(int(p)))
    except Exception:
        h1 = False

    try:
        p = sympy.sympify(witness)
        if not p.is_integer or not isprime(int(p)):
            neg_q = False
        else:
            coeff, factors = factor_list(x**4 + 1, modulus=int(p))
            # The polynomial is irreducible if it has exactly one factor and its multiplicity is 1
            neg_q = bool(len(factors) == 1 and factors[0][1] == 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The polynomial x^4 + 1 is irreducible over F_p"
]

N_HYP = 1
NEG_Q_INDEX = 1