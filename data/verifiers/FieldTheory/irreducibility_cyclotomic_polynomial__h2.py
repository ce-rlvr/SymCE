import sympy
from sympy.abc import x

def conditions(witness):
    """
    Check if the witness is a counterexample to the conjecture.
    """
    # H_1: n is a positive integer
    try:
        if isinstance(witness, bool):
            h1 = False
        elif not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = (n > 0)
    except Exception:
        h1 = False

    # ¬Q: Phi_n(x) is not irreducible over Q
    try:
        n = int(witness)
        poly = sympy.cyclotomic_poly(n, x)
        factors = sympy.factor_list(poly, domain='QQ')[1]
        is_irred = (len(factors) == 1 and factors[0][1] == 1)
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: Phi_n(x) is not irreducible over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1