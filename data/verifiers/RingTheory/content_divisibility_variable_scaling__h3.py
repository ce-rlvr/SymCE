import sympy as sp

x, y, z, t = sp.symbols('x y z t')

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a polynomial over R",
    "¬Q: The content of f does not divide the content of f evaluated at cx"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R_wit, f, c = witness
            if isinstance(f, sp.Poly):
                f_expr = f.as_expr()
            else:
                f_expr = sp.sympify(f)
            c_expr = sp.sympify(c)
            poly_f = sp.Poly(f_expr, x, domain=R_wit)
        elif isinstance(witness, tuple) and len(witness) == 2:
            f, c = witness
            if isinstance(f, sp.Poly):
                poly_f = f
                f_expr = f.as_expr()
            else:
                f_expr = sp.sympify(f)
                poly_f = sp.Poly(f_expr, x)
            c_expr = sp.sympify(c)
        else:
            return [False, False, False]
            
        R = poly_f.domain
        h1 = bool(R.is_UFD)
        h2 = True
        
        f_cx = f_expr.subs(x, c_expr * x)
        try:
            poly_fcx = sp.Poly(f_cx, x, domain=R)
            content_fcx = poly_fcx.content()
            content_f = poly_f.content()
            
            if content_f == 0 and content_fcx == 0:
                divides = True
            elif content_f == 0:
                divides = False
            else:
                try:
                    R.exquo(content_fcx, content_f)
                    divides = True
                except Exception:
                    divides = False
        except Exception:
            divides = False
            
        neg_q = not divides
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]