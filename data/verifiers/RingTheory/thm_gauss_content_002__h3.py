import sympy
from sympy import symbols, Poly
from sympy.abc import x, y, z, a, b, c, t

X, Y = symbols('X Y')

def conditions(witness):
    try:
        f = sympy.sympify(witness)
        if not isinstance(f, sympy.Expr):
            return [False, False, False]
        
        free_syms = f.free_symbols
        if X in free_syms:
            var_X = X
        elif x in free_syms:
            var_X = x
        elif free_syms:
            # Sort to ensure determinism
            var_X = sorted(list(free_syms), key=lambda s: s.name)[0]
        else:
            var_X = x
            
        try:
            poly_f = Poly(f, var_X)
        except Exception:
            return [False, False, False]
            
        # H1: R is a UFD
        try:
            domain = poly_f.domain
            h1 = domain.is_UFD
        except Exception:
            h1 = False
            
        # H2: f is a non-zero polynomial of degree d
        try:
            h2 = (f != 0)
        except Exception:
            h2 = False
            
        # neg_Q: content of F is not equal to content of f
        # The content of the homogenization F in (R[X])[Y] is X^k * c(f),
        # where k is the minimum degree of a non-zero term in f.
        # This equals c(f) if and only if k = 0 (i.e., the constant term is non-zero).
        try:
            d = poly_f.degree()
            if d < 0:
                neg_q = False
            else:
                coeffs = poly_f.all_coeffs()
                min_power = 0
                for j in range(d + 1):
                    if coeffs[d - j] != 0:
                        min_power = j
                        break
                neg_q = (min_power > 0)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial of degree d",
    "¬Q: The content of F is not equal to the content of f"
]

N_HYP = 2
NEG_Q_INDEX = 2