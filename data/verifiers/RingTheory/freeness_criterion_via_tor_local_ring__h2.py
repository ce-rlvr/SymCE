import sympy
from sympy.ntheory import isprime

class Z_localization:
    """Representation of the localization of Z at a prime ideal (p)."""
    def __init__(self, p):
        self.p = p

class Q_module:
    """Representation of the module of rational numbers Q."""
    pass

class PolynomialLocalization:
    """Representation of the localization of k[x] at the ideal (x)."""
    pass

class RationalFunctionModule:
    """Representation of the module of rational functions k(x)."""
    pass

# Named object bindings for the witness expression to reference
Z_loc_2 = Z_localization(2)
Z_loc_3 = Z_localization(3)
Z_loc_5 = Z_localization(5)
Q_mod = Q_module()
k_x_loc = PolynomialLocalization()
k_x_frac = RationalFunctionModule()

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        R, M = witness
    except Exception:
        return [False, False, False]
        
    def is_Q(m):
        return isinstance(m, Q_module) or m == sympy.S.Rationals

    # H_1: R is a commutative local ring with maximal ideal m
    h1 = False
    try:
        if isinstance(R, Z_localization):
            h1 = bool(isprime(R.p))
        elif isinstance(R, PolynomialLocalization):
            h1 = True
        elif R in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
    except Exception:
        pass

    # H_2: Tor_1^R(M, R/m) = 0
    h2 = False
    try:
        if is_Q(M) and isinstance(R, Z_localization):
            h2 = True
        elif isinstance(M, RationalFunctionModule) and isinstance(R, PolynomialLocalization):
            h2 = True
        elif R in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h2 = True
        elif isinstance(M, Z_localization) and isinstance(R, Z_localization) and R.p == M.p:
            h2 = True
    except Exception:
        pass

    # ¬Q: M is not a free R-module
    neg_q = False
    try:
        if is_Q(M) and isinstance(R, Z_localization):
            neg_q = True
        elif isinstance(M, RationalFunctionModule) and isinstance(R, PolynomialLocalization):
            neg_q = True
        elif R in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            neg_q = False
        elif isinstance(M, Z_localization) and isinstance(R, Z_localization) and R.p == M.p:
            neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring with maximal ideal m",
    "H_2: Tor_1^R(M, R/m) = 0",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2