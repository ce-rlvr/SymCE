import sympy
from sympy import Poly, discriminant, sympify, factor_list
from sympy.abc import x, y, z, t

# Setup
Q = sympy.QQ
R = sympy.RR
Z = sympy.ZZ

def conditions(witness):
    try:
        if hasattr(witness, 'as_expr'):
            f = witness.as_expr()
        else:
            f = sympify(witness)
    except Exception:
        return [False, False]
    
    # H_1: f(x) is irreducible over R
    h1 = False
    try:
        if not f.is_number:
            vars = list(f.free_symbols)
            if len(vars) > 0:
                p_check = Poly(f, *vars)
                # Ensure all coefficients are real numbers
                if all(c.is_real for c in p_check.coeffs()):
                    if len(vars) == 1:
                        v = vars[0]
                        p = Poly(f, v)
                        d = p.degree()
                        if d == 1:
                            h1 = True
                        elif d == 2:
                            disc = discriminant(f, v)
                            h1 = bool(disc < 0)
                    elif len(vars) > 1:
                        # Multivariable case (the dropped hypothesis was "in one variable")
                        p = Poly(f, *vars)
                        # Homogeneous polynomials of degree > 2 in multiple variables are reducible over R
                        if p.is_homogeneous and p.total_degree() > 2:
                            h1 = False
                        else:
                            # If it is absolutely irreducible, it won't factor over Q either.
                            # factor_list over Q is a reliable proxy for the verifier here.
                            facs = factor_list(f)
                            if len(facs[1]) == 1 and facs[1][0][1] == 1:
                                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The degree of f(x) is NOT 1 and NOT 2
    neg_q = False
    try:
        if not f.is_number:
            p = Poly(f)
            d = p.total_degree()
            if d != 1 and d != 2:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is irreducible over R",
    "¬Q: The degree of f(x) is not 1 and not 2"
]

N_HYP = 1
NEG_Q_INDEX = 1