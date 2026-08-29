import sympy
from sympy import minpoly, degree, sqrt, Rational, I

# Top-level setup for witness evaluation
# The witness is expected to be a tuple: (alpha, beta, gamma, m, n)
# where alpha, beta, gamma are algebraic numbers (e.g., using sqrt, Rational, I)
# and m, n are integers.

def conditions(witness) -> list[bool]:
    try:
        alpha, beta, gamma, m, n = witness
    except Exception:
        return [False] * 6

    # H_1: E/F is a field extension
    # Implicitly true for Q and its algebraic extensions in C.
    h1 = True

    # H_2: alpha and beta are algebraic over F
    try:
        poly_alpha = minpoly(alpha)
        poly_beta = minpoly(beta)
        h2 = True
    except Exception:
        h2 = False
        poly_alpha = None
        poly_beta = None

    # H_3: The degree of the minimal polynomial of alpha over F is m
    try:
        h3 = h2 and (degree(poly_alpha) == m)
    except Exception:
        h3 = False

    # H_4: The degree of the minimal polynomial of beta over F is n
    try:
        h4 = h2 and (degree(poly_beta) == n)
    except Exception:
        h4 = False

    # H_5: gamma is a primitive element such that F(alpha, beta) = F(gamma)
    try:
        poly_gamma = minpoly(gamma)
        d1 = degree(poly_gamma)
    except Exception:
        d1 = None

    try:
        if d1 is None:
            h5 = False
        else:
            # Compute d2 = [F(alpha, beta) : F]
            d2 = 0
            for c in range(1, 8):
                p = minpoly(alpha + c * beta)
                d2 = max(d2, degree(p))
                
            # Compute d3 = [F(alpha, beta, gamma) : F]
            d3 = d2
            for c1 in range(1, 4):
                for c2 in range(1, 4):
                    p = minpoly(alpha + c1 * beta + c2 * gamma)
                    d3 = max(d3, degree(p))
                    
            # F(gamma) = F(alpha, beta) iff their degrees over F are equal
            # and gamma is in F(alpha, beta) (which means d2 == d3).
            h5 = (d1 == d2) and (d2 == d3)
    except Exception:
        h5 = False

    # ¬Q: The degree of the minimal polynomial of gamma over F is not mn
    try:
        if d1 is not None:
            neg_q = (d1 != m * n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "H_2: alpha and beta are algebraic over F",
    "H_3: The degree of the minimal polynomial of alpha over F is m",
    "H_4: The degree of the minimal polynomial of beta over F is n",
    "H_5: gamma is a primitive element such that F(alpha, beta) = F(gamma)",
    "¬Q: The degree of the minimal polynomial of gamma over F is not mn"
]

N_HYP = 5
NEG_Q_INDEX = 5