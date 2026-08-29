import sympy
from sympy.abc import x, y

# Top-level setup
# No specific named groups needed for this ring theory theorem.
# We use sympy.abc.x and sympy.abc.y for the polynomial variables.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, f = witness
        else:
            f = witness
            
        f = sympy.sympify(f)
        if not isinstance(f, sympy.Expr):
            return [False, False, False]
            
        free_vars = f.free_symbols
        if not free_vars.issubset({x, y}):
            return [False, False, False]
            
        P_expr = sympy.expand(y - f)
        if not P_expr.is_polynomial(x, y):
            return [False, False, False]
            
        H1 = True
        H2 = True
        
        P_poly = sympy.poly(P_expr, x, y, domain='QQ')
        if P_poly is None or P_poly.is_zero or P_poly.is_constant():
            is_iso = False
        else:
            factors = sympy.factor_list(P_expr)
            if len(factors[1]) > 1 or factors[1][0][1] > 1:
                is_iso = False
            else:
                deg_x = sympy.degree(P_expr, x)
                deg_y = sympy.degree(P_expr, y)
                if deg_x == 1 and sympy.poly(P_expr.coeff(x, 1), y).is_constant():
                    is_iso = True
                elif deg_y == 1 and sympy.poly(P_expr.coeff(y, 1), x).is_constant():
                    is_iso = True
                else:
                    is_iso = False
                    
        neg_Q = not is_iso
        
        return [H1, H2, neg_Q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Polynomial ring in two variables over R",
    "neg_Q: Factor ring is not isomorphic to polynomial ring in one variable"
]

N_HYP = 2
NEG_Q_INDEX = 2