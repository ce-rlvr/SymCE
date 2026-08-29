import sympy
from sympy import QQ, Poly, gcd, expand
from sympy.abc import x

GF2 = sympy.GF(2)
GF3 = sympy.GF(3)
GF5 = sympy.GF(5)
GF7 = sympy.GF(7)

def conditions(witness) -> list[bool]:
    H_1_ok = False
    H_2_ok = False
    neg_Q_ok = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            F, f_list, f = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            f_list, f = witness
            F = QQ
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(F, 'is_Field'):
            H_1_ok = bool(F.is_Field)
        elif hasattr(F, 'is_field'):
            H_1_ok = bool(F.is_field)
    except Exception:
        H_1_ok = False
        
    try:
        symbols = set()
        if hasattr(f, 'free_symbols'):
            symbols.update(f.free_symbols)
        if isinstance(f_list, (list, tuple)):
            for fi in f_list:
                if hasattr(fi, 'free_symbols'):
                    symbols.update(fi.free_symbols)
        
        if x in symbols:
            var = x
        elif len(symbols) > 0:
            var = list(symbols)[0]
        else:
            var = x
    except Exception:
        var = x

    try:
        if isinstance(f_list, (list, tuple)):
            product = 1
            for fi in f_list:
                product = product * fi
            
            try:
                poly_f = Poly(f, var, domain=F)
                poly_prod = Poly(product, var, domain=F)
                if poly_f == poly_prod:
                    H_2_ok = True
            except Exception:
                if expand(f - product) == 0:
                    H_2_ok = True
    except Exception:
        H_2_ok = False
        
    try:
        if H_1_ok and H_2_ok:
            is_coprime = True
            for i in range(len(f_list)):
                for j in range(i + 1, len(f_list)):
                    try:
                        pi = Poly(f_list[i], var, domain=F)
                        pj = Poly(f_list[j], var, domain=F)
                        g = pi.gcd(pj)
                        if g.is_zero or g.degree() > 0:
                            is_coprime = False
                            break
                    except Exception:
                        expr_i = f_list[i].as_expr() if hasattr(f_list[i], 'as_expr') else f_list[i]
                        expr_j = f_list[j].as_expr() if hasattr(f_list[j], 'as_expr') else f_list[j]
                        g = gcd(expr_i, expr_j)
                        g_poly = Poly(g, var)
                        if g_poly.is_zero or g_poly.degree() > 0:
                            is_coprime = False
                            break
                if not is_coprime:
                    break
            neg_Q_ok = not is_coprime
    except Exception:
        neg_Q_ok = False
        
    return [H_1_ok, H_2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is the product f_1 f_2 ... f_k",
    "¬Q: quotient ring is not isomorphic to the direct product"
]

N_HYP = 2
NEG_Q_INDEX = 2