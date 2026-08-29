import sympy
from sympy.abc import x

def conditions(witness):
    try:
        n = int(witness)
        h1 = bool(n == witness and n > 0 and not isinstance(witness, bool))
    except Exception:
        h1 = False

    try:
        n = int(witness)
        poly = sympy.cyclotomic_poly(n, x)
        factors = sympy.factor_list(poly, domain='QQ')[1]
        # A polynomial is irreducible if it has exactly one factor and its multiplicity is 1
        is_irreducible = (len(factors) == 1 and factors[0][1] == 1)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: \\Phi_n(x) is not irreducible over \\mathbb{Q}"
]

N_HYP = 1
NEG_Q_INDEX = 1