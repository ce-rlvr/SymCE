import sympy as sp

x = sp.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, sp.Poly):
            f_expr = witness.as_expr()
        else:
            f_expr = sp.sympify(witness)
            
        free_symbols = f_expr.free_symbols
        if len(free_symbols) > 1:
            h1 = False
            var = x
        elif len(free_symbols) == 1:
            var = list(free_symbols)[0]
            h1 = f_expr.is_polynomial(var)
        else:
            var = x
            h1 = f_expr.is_polynomial(var)
    except Exception:
        h1 = False
        var = x
        f_expr = None

    if not h1 or f_expr is None:
        return [False, False]

    try:
        f_poly = sp.Poly(f_expr, var)
        degree = f_poly.degree()
        
        if degree <= 0:
            neg_q = False
        else:
            roots_dict = sp.roots(f_poly)
            if sum(roots_dict.values()) == degree:
                unique_roots = list(roots_dict.keys())
                neg_q = False
                for r in unique_roots:
                    r_conj = sp.conjugate(r)
                    is_root = False
                    for r2 in unique_roots:
                        diff = sp.simplify(r_conj - r2)
                        if diff == 0:
                            is_root = True
                            break
                        try:
                            if abs(complex(diff.evalf())) < 1e-9:
                                is_root = True
                                break
                        except Exception:
                            pass
                    if not is_root:
                        val = sp.simplify(f_expr.subs(var, r_conj))
                        if val != 0:
                            try:
                                val_num = complex(val.evalf())
                                if abs(val_num) > 1e-9:
                                    neg_q = True
                                    break
                            except Exception:
                                neg_q = True
                                break
            else:
                # Fallback for polynomials where sp.roots cannot find all roots
                f_der = sp.diff(f_expr, var)
                try:
                    g = sp.gcd(f_expr, f_der)
                    f_sq = sp.simplify(f_expr / g)
                except Exception:
                    f_sq = f_expr
                
                sq_poly = sp.Poly(f_sq, var)
                coeffs = sq_poly.all_coeffs()
                lead = coeffs[0]
                neg_q = False
                for c in coeffs:
                    c_monic = sp.simplify(c / lead)
                    im_c = sp.im(c_monic).simplify()
                    if im_c != 0:
                        try:
                            im_num = complex(im_c.evalf())
                            if abs(im_num) > 1e-9:
                                neg_q = True
                                break
                        except Exception:
                            neg_q = True
                            break
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial",
    "¬Q: Complex conjugation does not restrict to Gal(K/Q) or does not interchange the non-real complex conjugate roots of f(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1