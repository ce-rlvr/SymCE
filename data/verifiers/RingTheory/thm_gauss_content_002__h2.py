import sympy
from sympy import symbols, Poly, gcd_list

X, Y = symbols('X Y')

def conditions(witness):
    try:
        f, d = witness
    except Exception:
        return [False, False, False]
    
    try:
        f_poly = Poly(f, X)
        h1 = getattr(f_poly.domain, 'is_UFD', True)
    except Exception:
        h1 = False

    try:
        F = sympy.expand(Y**d * f.subs(X, X/Y))
        F_poly = Poly(F, X, Y)
        h2 = True
    except Exception:
        h2 = False

    try:
        c_f = gcd_list(Poly(f, X).coeffs())
        c_F = gcd_list(Poly(F, X).coeffs())
        
        if c_f == 0:
            neg_q = (c_F != 0)
        else:
            ratio = sympy.cancel(c_F / c_f)
            if ratio.free_symbols.intersection({X, Y}):
                neg_q = True
            else:
                if sympy.simplify(ratio - 1) == 0 or sympy.simplify(ratio + 1) == 0:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = ["H_1: R is a Unique Factorization Domain", "H_2: F is the homogenization of f", "neg_Q: The content of F is not equal to the content of f"]

N_HYP = 2
NEG_Q_INDEX = 2