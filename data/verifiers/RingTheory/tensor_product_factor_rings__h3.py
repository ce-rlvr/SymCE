import sympy

x, y = sympy.symbols('x y')
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            R, f, g = witness
        elif len(witness) == 2:
            R = ZZ
            f, g = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif hasattr(R, 'is_Ring') and R.is_Ring and R.is_commutative:
            h1 = True
        elif R in [ZZ, QQ, RR, CC]:
            h1 = True
        elif isinstance(R, sympy.polys.domains.Domain) and getattr(R, 'is_CommutativeRing', False):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: f(x) is a polynomial in R[x]
    try:
        x_sym = sympy.Symbol('x')
        f_expr = f
        if isinstance(f_expr, sympy.Poly):
            f_expr = f_expr.as_expr()
        else:
            f_expr = sympy.sympify(f_expr, locals={'x': x_sym})
        h2 = f_expr.is_polynomial(x_sym) and f_expr.free_symbols.issubset({x_sym})
    except Exception:
        h2 = False
        
    # neg_Q: conclusion fails
    # The conclusion holds if g(y) is a polynomial in R[y].
    # It fails if g(y) is not a polynomial in R[y] (e.g., contains x, or is not a polynomial).
    try:
        x_sym = sympy.Symbol('x')
        y_sym = sympy.Symbol('y')
        g_expr = g
        if isinstance(g_expr, sympy.Poly):
            g_expr = g_expr.as_expr()
        else:
            g_expr = sympy.sympify(g_expr, locals={'x': x_sym, 'y': y_sym})
        is_poly_y = g_expr.is_polynomial(y_sym) and g_expr.free_symbols.issubset({y_sym})
        neg_q = not is_poly_y
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f is a polynomial over R",
    "¬Q: The tensor product is not isomorphic to the joint quotient ring"
]

N_HYP = 2
NEG_Q_INDEX = 2