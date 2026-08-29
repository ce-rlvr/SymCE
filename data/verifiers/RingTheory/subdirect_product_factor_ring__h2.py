import sympy as sp

# Top-level setup
x = sp.Symbol('x')

def is_poly_in_Zx(expr):
    try:
        expr = sp.sympify(expr)
        if not isinstance(expr, sp.Expr):
            return False
        if not expr.free_symbols.issubset({x}):
            return False
        poly = sp.Poly(expr, x)
        return poly.domain == sp.ZZ
    except Exception:
        return False

def conditions(witness):
    h1_ok = False
    W = []
    try:
        if isinstance(witness, (list, tuple, set)):
            W = list(witness)
        else:
            W = [witness]
        
        if len(W) > 0:
            h1_ok = all(is_poly_in_Zx(w) for w in W)
    except Exception:
        h1_ok = False

    q_ok = False
    try:
        if h1_ok:
            W_sym = [sp.sympify(w) for w in W]
            
            try:
                gb = sp.groebner(W_sym, x, domain='ZZ')
                gb_list = list(gb)
                
                if len(gb_list) == 1:
                    P = gb_list[0]
                    poly = sp.Poly(P, x)
                    if poly.degree() == 2:
                        coeffs = poly.all_coeffs()
                        if coeffs[0] == -1:
                            coeffs = [-c for c in coeffs]
                        
                        if coeffs[0] == 1:
                            c1, c0 = coeffs[1], coeffs[2]
                            if c1**2 - 4*c0 == 9:
                                q_ok = True
            except Exception:
                g = W_sym[0]
                for w in W_sym[1:]:
                    g = sp.gcd(g, w)
                
                poly_g = sp.Poly(g, x)
                lc = poly_g.LC()
                P = sp.simplify(g / lc)
                poly_P = sp.Poly(P, x)
                
                if poly_P.domain == sp.ZZ and poly_P.degree() == 2:
                    coeffs = poly_P.all_coeffs()
                    c1, c0 = coeffs[1], coeffs[2]
                    if c1**2 - 4*c0 == 9:
                        if len(W_sym) == 1:
                            if abs(lc) == 1:
                                q_ok = True
                        else:
                            q_list = [sp.cancel(w / P) for w in W_sym]
                            for q in q_list:
                                if q == 1 or q == -1:
                                    q_ok = True
    except Exception:
        pass

    neg_q_ok = not q_ok

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: witness is a valid ideal in Z polynomial ring",
    "not Q: R mod I is NOT isomorphic to the subring of Z x Z with a = b mod 3"
]

N_HYP = 1
NEG_Q_INDEX = 1