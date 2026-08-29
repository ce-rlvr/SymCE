import sympy
from sympy import Poly, resultant, diff, rem

# Top-level setup: define symbols for the function fields
T, X, Y = sympy.symbols('T X Y')

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample.
    The witness should be a tuple: (p, poly_E, poly_K)
      - p: a prime integer (characteristic of the fields)
      - poly_E: a polynomial in X and T representing the minimal polynomial of E over F_p(T)
      - poly_K: a polynomial in Y, X, and T representing the minimal polynomial of K over E
    """
    try:
        p, poly_E, poly_K = witness
    except Exception:
        return [False, False, False]
        
    def is_zero_mod_p(expr, *gens):
        try:
            return Poly(expr, *gens, domain=sympy.GF(p)).is_zero
        except Exception:
            return False

    def is_irreducible_mod_p(expr, *gens):
        try:
            poly = Poly(expr, *gens, domain=sympy.GF(p))
            if poly.is_zero:
                return False
            num, factors = poly.factor_list()
            # Irreducible if there is exactly one factor and its multiplicity is 1
            return len(factors) == 1 and factors[0][1] == 1
        except Exception:
            return False

    # H_1: F, E, and K are fields such that F is a subfield of E, and E is a subfield of K.
    # We use F = F_p(T). E = F[X]/(poly_E). K = E[Y]/(poly_K).
    h1_ok = False
    try:
        if sympy.isprime(p):
            poly_E_poly = Poly(poly_E, X)
            poly_K_poly = Poly(poly_K, Y)
            # Enforce monicity over ZZ to prevent degree drops mod p and ensure safe resultants
            if poly_E_poly.LC() == 1 and poly_K_poly.LC() == 1:
                deg_E = poly_E_poly.degree()
                deg_K = poly_K_poly.degree()
                if deg_E >= 1 and deg_K >= 1:
                    # Check if E is a field (poly_E is irreducible over F_p(T))
                    if is_irreducible_mod_p(poly_E, X, T):
                        # Check if K is a field by computing the resultant to find the minimal poly of Y over F_p(T)
                        res = resultant(poly_E, poly_K, X)
                        if is_irreducible_mod_p(res, Y, T):
                            if sympy.degree(res, Y) == deg_E * deg_K:
                                h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: Every element of K is algebraic and separable over E.
    # This holds iff the generator Y is separable over E, meaning diff(poly_K, Y) != 0 mod p in E.
    h2_ok = False
    try:
        if h1_ok:
            deriv_K = diff(poly_K, Y)
            rem_deriv = rem(deriv_K, poly_E, X)
            if not is_zero_mod_p(rem_deriv, X, Y, T):
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion fails (K contains an element that is not separable over F).
    # This holds iff K/F is inseparable, which means the minimal polynomial of Y over F_p(T) has derivative 0 mod p.
    neg_q_ok = False
    try:
        if h1_ok:
            res = resultant(poly_E, poly_K, X)
            deriv_res = diff(res, Y)
            if is_zero_mod_p(deriv_res, Y, T):
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F, E, and K are fields such that F is a subfield of E, and E is a subfield of K",
    "H_2: Every element of K is algebraic and separable over E",
    "¬Q: K contains an element that is not separable over F"
]

N_HYP = 2
NEG_Q_INDEX = 2