import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy.ntheory import factorint
import math

# Top-level setup
Q = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Witness is expected to be a tuple (n, P) where:
      - n is an integer (the order of the root of unity)
      - P is a SymPy polynomial expression over Q
    F is implicitly Q, and E is implicitly the splitting field of P over Q.
    (If witness is just P, n defaults to 2).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, P = witness
        else:
            n = 2
            P = witness
            
        if isinstance(P, (list, tuple)):
            P = math.prod(sympy.sympify(p) for p in P)
        else:
            P = sympy.sympify(P)
    except Exception:
        return [False, False, False]
        
    # H_1: F contains a primitive n-th root of unity
    # For F = Q, the only primitive n-th roots of unity are for n = 1 and n = 2.
    try:
        h1 = bool(n in [1, 2])
    except Exception:
        h1 = False
        
    # H_2: E is a Galois extension of F
    # The splitting field of any polynomial over Q is a Galois extension of Q.
    # We just verify that P is a valid non-constant polynomial.
    try:
        symbols = list(P.free_symbols)
        if len(symbols) == 1:
            gen = symbols[0]
            poly_P = Poly(P, gen, domain='QQ')
        elif len(symbols) == 0:
            poly_P = Poly(P, x, domain='QQ')
        else:
            poly_P = None
            
        if poly_P is not None:
            h2 = bool(poly_P.degree() >= 1)
        else:
            h2 = False
    except Exception:
        h2 = False
        poly_P = None
        
    # ¬Q: E is not the splitting field of x^n - a over F for any a in F
    # The splitting field of x^n - a over Q has degree at most n (since n <= 2).
    # If P has an irreducible factor of degree > n, or multiple independent quadratic factors,
    # then the splitting field E has degree > n. Thus E cannot be the splitting field of x^n - a.
    try:
        neg_q = False
        if poly_P is not None:
            factors = poly_P.factor_list()[1]
            if any(f.degree() > n for f, _ in factors):
                neg_q = True
            elif n == 2:
                radicals = set()
                for f, _ in factors:
                    if f.degree() == 2:
                        coeffs = f.all_coeffs()
                        a, b, c = coeffs[0], coeffs[1], coeffs[2]
                        disc = sympy.sympify(b**2 - 4*a*c)
                        if disc != 0:
                            num, den = disc.as_numer_denom()
                            val = abs(num * den)
                            core = 1
                            for p, exp in factorint(val).items():
                                if exp % 2 == 1:
                                    core *= p
                            if disc < 0:
                                core = -core
                            if core != 1:
                                radicals.add(core)
                if len(radicals) >= 2:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F contains a primitive n-th root of unity",
    "H_2: E is a Galois extension of F",
    "¬Q: E is not the splitting field of x^n - a over F for any a in F"
]

N_HYP = 2
NEG_Q_INDEX = 2