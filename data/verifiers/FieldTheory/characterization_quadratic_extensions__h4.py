import sympy
from sympy import Symbol, Poly, isprime, QQ, ZZ, GF

x = Symbol('x')

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The characteristic of F is not equal to 2",
    "H_3: E/F is a field extension",
    "¬Q: E is not of the form F(alpha) where alpha^2 = d for some non-square d in F"
]

def conditions(witness):
    poly_expr = None
    p = 0

    try:
        # Parse the witness into a minimal polynomial and a characteristic p
        if isinstance(witness, (int, sympy.Integer)):
            poly_expr = x**int(witness) - 2
            p = 0
        elif hasattr(witness, 'ext') and hasattr(witness.ext, 'minpoly'):
            poly_expr = witness.ext.minpoly.as_expr()
            p = 0
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            a, b = witness
            
            if isinstance(a, (int, sympy.Integer)) and hasattr(b, 'char'):
                poly_expr = x**int(a) - 2
                p = int(b.char)
            elif isinstance(b, (int, sympy.Integer)) and hasattr(a, 'char'):
                poly_expr = x**int(b) - 2
                p = int(a.char)
            elif isinstance(a, (int, sympy.Integer)) and b == sympy.QQ:
                poly_expr = x**int(a) - 2
                p = 0
            elif isinstance(b, (int, sympy.Integer)) and a == sympy.QQ:
                poly_expr = x**int(b) - 2
                p = 0
            else:
                if isinstance(a, (int, sympy.Integer)):
                    p = int(a)
                elif isinstance(b, (int, sympy.Integer)):
                    p = int(b)
                elif hasattr(a, 'char'):
                    p = int(a.char)
                elif hasattr(b, 'char'):
                    p = int(b.char)
                else:
                    p = 0
                    
                if hasattr(a, 'ext') and hasattr(a.ext, 'minpoly'):
                    poly_expr = a.ext.minpoly
                elif hasattr(b, 'ext') and hasattr(b.ext, 'minpoly'):
                    poly_expr = b.ext.minpoly
                elif hasattr(a, 'free_symbols') and not hasattr(b, 'free_symbols'):
                    poly_expr = a
                elif hasattr(b, 'free_symbols') and not hasattr(a, 'free_symbols'):
                    poly_expr = b
                elif isinstance(a, (int, sympy.Integer)) and hasattr(b, 'free_symbols'):
                    poly_expr = b
                elif isinstance(b, (int, sympy.Integer)) and hasattr(a, 'free_symbols'):
                    poly_expr = a
                else:
                    poly_expr = a
        else:
            poly_expr = witness
            
        if hasattr(poly_expr, 'as_expr'):
            poly_expr = poly_expr.as_expr()
    except Exception:
        pass

    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    try:
        if poly_expr is not None:
            syms = list(poly_expr.free_symbols)
            sym = syms[0] if len(syms) == 1 else x
            
            if p == 0:
                h1 = True
                h2 = True
                poly = sympy.Poly(poly_expr, sym, domain='QQ')
                h3 = poly.degree() >= 1 and poly.is_irreducible
                neg_q = (poly.degree() != 2)
            else:
                h1 = sympy.isprime(p)
                h2 = (p != 2)
                poly = sympy.Poly(poly_expr, sym, modulus=p)
                h3 = poly.degree() >= 1 and poly.is_irreducible
                neg_q = (poly.degree() != 2)
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]