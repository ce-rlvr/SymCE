import sympy
from sympy import ZZ, QQ, RR, CC, Rational, Dummy, Poly, minpoly

# Top-level setup
# Standard domains are imported above. The witness should provide SymPy Domain objects
# for R, F, E (e.g., ZZ, QQ) and a SymPy expression for alpha.

def conditions(witness) -> list[bool]:
    try:
        R = witness['R']
        F = witness['F']
        E = witness['E']
        alpha = witness['alpha']
    except Exception:
        return [False, False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H_2: F is the field of fractions of R
    try:
        h2 = bool(F == R.get_field())
    except Exception:
        h2 = False

    # H_3: E is a field extension of F
    try:
        h3 = False
        if getattr(E, 'is_Field', False):
            if E == F:
                h3 = True
            else:
                try:
                    h3 = bool(E.unify(F) == E)
                except Exception:
                    h3 = True
    except Exception:
        h3 = False

    # ¬Q: The minimal polynomial of alpha over F does NOT have all its coefficients in R
    try:
        x = Dummy('x')
        mp = minpoly(alpha, x, domain=F)
        poly_mp = Poly(mp, x)
        coeffs = poly_mp.all_coeffs()
        
        coeffs_in_R = all((c in R) for c in coeffs)
        neg_q = not coeffs_in_R
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: F is the field of fractions of R",
    "H_3: E is a field extension of F",
    "¬Q: The minimal polynomial of alpha over F does not have all its coefficients in R"
]

N_HYP = 3
NEG_Q_INDEX = 3