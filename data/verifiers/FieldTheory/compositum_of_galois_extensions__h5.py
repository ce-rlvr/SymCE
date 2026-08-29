import sympy
from sympy import Dummy, factor, degree, Mul, Pow, minpoly
from sympy import Rational, sqrt, cbrt, I, pi, exp

# Top-level setup
# F is implicitly QQ. The witness should be a tuple (a, b) of algebraic numbers
# generating K = QQ(a) and L = QQ(b).

def _splits_completely(expr, x, exts):
    try:
        factored = factor(expr, extension=exts)
        if isinstance(factored, Mul):
            args = factored.args
        else:
            args = [factored]
        for arg in args:
            if arg.has(x):
                if isinstance(arg, Pow):
                    base = arg.base
                else:
                    base = arg
                if degree(base, x) > 1:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False] * 5
        
    x = Dummy('x')
    
    # H_1: F is a field
    # We implicitly use F = QQ, which is a field.
    h1 = True
    
    # H_2: K and L are finite field extensions of F
    try:
        poly_a = minpoly(a, x)
        poly_b = minpoly(b, x)
        h2 = poly_a.has(x) and poly_b.has(x)
    except Exception:
        h2 = False
        
    # H_3: K and L are contained in a common extension field
    # Algebraic numbers over QQ can always be embedded in C.
    h3 = True
    
    # H_4: K/F is a Galois extension
    try:
        h4 = _splits_completely(poly_a, x, [a])
    except Exception:
        h4 = False
        
    # ¬Q: The compositum field KL is not a Galois extension of F
    # KL is Galois over F iff the minimal polynomials of its generators split completely in KL.
    try:
        kl_galois = _splits_completely(poly_a, x, [a, b]) and _splits_completely(poly_b, x, [a, b])
        neg_q = not kl_galois
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K and L are finite field extensions of F",
    "H_3: K and L are contained in a common extension field",
    "H_4: K/F is a Galois extension",
    "¬Q: The compositum field KL is not a Galois extension of F"
]

N_HYP = 4
NEG_Q_INDEX = 4