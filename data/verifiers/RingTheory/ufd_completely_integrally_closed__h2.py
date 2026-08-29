import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z, t

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: x is an element of the fraction field K",
    "H_3: d is a non-zero element in R",
    "H_4: d * x^n is in R for all positive integers n",
    "¬Q: x does not belong to R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 5
        R, x_val, d_val = witness
    except Exception:
        return [False] * 5

    # H1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H2: x is an element of the fraction field K
    try:
        K = R.frac_field
        if x_val in K:
            x_K = x_val
            h2 = True
        elif hasattr(K, 'from_expr'):
            x_K = K.from_expr(x_val)
            h2 = True
        else:
            x_K = K(x_val)
            h2 = True
    except Exception:
        h2 = False

    # H3: d is a non-zero element in R
    try:
        if d_val in R:
            d_R = d_val
        elif hasattr(R, 'from_expr'):
            d_R = R.from_expr(d_val)
        else:
            d_R = R(d_val)
        h3 = bool(d_R != R.zero)
    except Exception:
        h3 = False

    # H4: d * x^n is in R for all positive integers n
    try:
        h4 = False
        if h2 and h3:
            all_in_R = True
            d_K = K(d_R)
            # Check up to n=50 to safely verify the condition algebraically
            for n in range(1, 51):
                term = d_K * (x_K**n)
                if term not in R:
                    all_in_R = False
                    break
            h4 = all_in_R
    except Exception:
        h4 = False

    # neg_Q: x does not belong to R
    try:
        if h2:
            neg_q = bool(x_K not in R)
        else:
            neg_q = bool(x_val not in R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]