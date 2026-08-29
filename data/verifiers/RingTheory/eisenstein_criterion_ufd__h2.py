import sympy
from sympy import Poly, Symbol, isprime
from sympy.polys.polytools import factor_list

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false Eisenstein's Criterion conjecture.
    The witness should be a tuple (p, f) where:
      - p is a prime integer
      - f is a SymPy expression in x representing the polynomial
    """
    try:
        p, f = witness
    except Exception:
        return [False] * 6

    # H1: R is a Unique Factorization Domain with fraction field K
    # We restrict our check to R = Z, which is a UFD.
    try:
        p_val = int(p)
        f_poly = Poly(f, x)
        coeffs = f_poly.all_coeffs()
        h1 = all(sympy.sympify(c).is_integer for c in coeffs)
    except Exception:
        h1 = False

    # H2: p is a prime element in R
    try:
        h2 = isprime(abs(p_val))
    except Exception:
        h2 = False

    # H3: p divides a_i for all 0 <= i < n
    try:
        n = f_poly.degree()
        if n < 0:
            h3 = False
        else:
            # coeffs are [a_n, a_{n-1}, ..., a_0]
            a_i_list = coeffs[1:]
            h3 = all(sympy.sympify(a) % p_val == 0 for a in a_i_list)
    except Exception:
        h3 = False

    # H4: p does not divide a_n
    try:
        if n < 0:
            h4 = False
        else:
            a_n = coeffs[0]
            h4 = (sympy.sympify(a_n) % p_val != 0)
    except Exception:
        h4 = False

    # H5: p^2 does not divide a_0
    try:
        if n < 0:
            h5 = False
        else:
            a_0 = coeffs[-1]
            h5 = (sympy.sympify(a_0) % (p_val**2) != 0)
    except Exception:
        h5 = False

    # ¬Q: The polynomial f(x) is not irreducible over the fraction field K
    try:
        if n <= 0:
            # Constant polynomials (degree <= 0) are units or zero in K[x], hence not irreducible.
            neg_q = True
        else:
            # Check irreducibility over Q
            factors = factor_list(f_poly, domain='QQ')[1]
            # Irreducible if there is exactly one prime factor with multiplicity 1
            is_irreducible = (len(factors) == 1 and factors[0][1] == 1)
            neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain with fraction field K",
    "H_2: p is a prime element in R",
    "H_3: p divides a_i for all 0 <= i < n",
    "H_4: p does not divide a_n",
    "H_5: p^2 does not divide a_0",
    "¬Q: The polynomial f(x) is not irreducible over the fraction field K"
]

N_HYP = 5
NEG_Q_INDEX = 5