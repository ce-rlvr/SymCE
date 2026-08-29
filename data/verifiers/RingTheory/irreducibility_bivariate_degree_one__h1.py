import sympy as sp
from sympy.abc import x, y

def is_poly_unit(poly):
    try:
        domain = poly.domain
        const_term = domain.zero
        for monom, c in poly.terms():
            if sum(monom) == 0:
                const_term = c
                break
                
        try:
            domain.invert(const_term)
            const_is_unit = True
        except Exception:
            const_is_unit = (abs(const_term) == 1)
            
        if not const_is_unit:
            return False
            
        for monom, c in poly.terms():
            if sum(monom) > 0:
                is_nilp = False
                for k in range(1, 20):
                    if c**k == domain.zero:
                        is_nilp = True
                        break
                if not is_nilp:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            f_poly, factor1, factor2 = witness
            domain = f_poly.domain
            is_tuple_witness = True
        elif isinstance(witness, sp.Poly):
            f_poly = witness
            domain = f_poly.domain
            is_tuple_witness = False
        else:
            f_expr = sp.sympify(witness)
            f_poly = sp.Poly(f_expr, x, y)
            domain = f_poly.domain
            is_tuple_witness = False
    except Exception:
        return [False, False, False, False]

    # H1: f(x,y) is a polynomial in K[x,y] of the form g(x)y + h(x)
    try:
        if not set(f_poly.gens).issubset({x, y}):
            h1_ok = False
        else:
            y_idx = f_poly.gens.index(y) if y in f_poly.gens else -1
            x_idx = f_poly.gens.index(x) if x in f_poly.gens else -1
            
            if y_idx != -1:
                deg_y = max([monom[y_idx] for monom in f_poly.monoms()]) if f_poly.monoms() else 0
            else:
                deg_y = 0
                
            if deg_y != 1:
                h1_ok = False
            else:
                g_terms = {}
                h_terms = {}
                h1_ok = True
                for monom, c in f_poly.terms():
                    y_pow = monom[y_idx] if y_idx != -1 else 0
                    x_pow = monom[x_idx] if x_idx != -1 else 0
                    
                    other_pow = sum(monom) - y_pow - x_pow
                    if other_pow > 0:
                        h1_ok = False
                        break
                        
                    if y_pow == 1:
                        g_terms[(x_pow,)] = c
                    elif y_pow == 0:
                        h_terms[(x_pow,)] = c
                    else:
                        h1_ok = False
                        break
                        
                if h1_ok:
                    g_poly_x = sp.Poly.from_dict(g_terms, x, domain=domain)
                    h_poly_x = sp.Poly.from_dict(h_terms, x, domain=domain)
    except Exception:
        h1_ok = False

    # H2: g(x) and h(x) are relatively prime in K[x]
    try:
        if h1_ok:
            try:
                gcd_gh = g_poly_x.gcd(h_poly_x)
                if is_poly_unit(gcd_gh):
                    h2_ok = True
                else:
                    h2_ok = False
            except Exception:
                if is_poly_unit(g_poly_x) or is_poly_unit(h_poly_x):
                    h2_ok = True
                else:
                    h2_ok = False
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # H3: g(x) is not the zero polynomial
    try:
        if h1_ok:
            h3_ok = not g_poly_x.is_zero
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: f(x,y) is NOT irreducible in K[x,y]
    try:
        if h1_ok:
            if is_poly_unit(f_poly):
                neg_q_ok = True
            elif is_tuple_witness:
                if f_poly == factor1 * factor2:
                    if not is_poly_unit(factor1) and not is_poly_unit(factor2):
                        neg_q_ok = True
                    else:
                        neg_q_ok = False
                else:
                    neg_q_ok = False
            else:
                try:
                    content, factors = sp.factor_list(f_poly)
                    try:
                        domain.invert(content)
                        content_is_unit = True
                    except Exception:
                        content_is_unit = (abs(content) == 1)
                        
                    is_irreducible = content_is_unit and (len(factors) == 1) and (factors[0][1] == 1)
                    neg_q_ok = not is_irreducible
                except Exception:
                    neg_q_ok = False
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a polynomial in x and y of the form g y + h",
    "H_2: g and h are relatively prime polynomials in x",
    "H_3: g is not the zero polynomial",
    "¬Q: f is not irreducible"
]

N_HYP = 3
NEG_Q_INDEX = 3