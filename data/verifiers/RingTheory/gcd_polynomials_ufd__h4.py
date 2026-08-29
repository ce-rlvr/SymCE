import sympy as sp

x, y, z = sp.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            c_f = witness.get('c_f', sp.Poly(f).content() if f is not None else None)
            c_g = witness.get('c_g', sp.Poly(g).content() if g is not None else None)
            f_1 = witness.get('f_1')
            g_1 = witness.get('g_1')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 6:
                f, g, c_f, c_g, f_1, g_1 = witness
            elif len(witness) == 4:
                f, g, f_1, g_1 = witness
                c_f = sp.Poly(f).content()
                c_g = sp.Poly(g).content()
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def are_associate(p1, p2, dom):
        p1 = sp.sympify(p1)
        p2 = sp.sympify(p2)
        if p1 == p2 or p1 == -p2:
            return True
        try:
            if p1.is_zero and p2.is_zero:
                return True
            if p1.is_zero or p2.is_zero:
                return False
            q = sp.cancel(p1 / p2)
            if dom.is_Field:
                return q.is_constant() and not q.is_zero
            else:
                q_dom = dom.from_sympy(q)
                return dom.is_unit(q_dom)
        except Exception:
            return False

    try:
        poly_f = sp.Poly(f)
        poly_g = sp.Poly(g)
        h1 = bool(poly_f.domain.is_UFD and poly_g.domain.is_UFD and poly_f.domain == poly_g.domain)
    except Exception:
        h1 = False

    try:
        poly_f = sp.Poly(f)
        poly_g = sp.Poly(g)
        h2 = bool(not poly_f.is_zero and not poly_g.is_zero)
    except Exception:
        h2 = False

    try:
        poly_f = sp.Poly(f)
        poly_g = sp.Poly(g)
        actual_c_f = poly_f.content()
        actual_c_g = poly_g.content()
        
        c_f_sym = sp.sympify(c_f)
        c_g_sym = sp.sympify(c_g)
        
        domain = poly_f.domain
        
        h3 = bool(are_associate(c_f_sym, actual_c_f, domain) and
                  are_associate(c_g_sym, actual_c_g, domain))
    except Exception:
        h3 = False

    try:
        expr_f = sp.sympify(f)
        expr_g = sp.sympify(g)
        gcd_fg = sp.gcd(expr_f, expr_g)
        
        expr_f1 = sp.sympify(f_1)
        expr_g1 = sp.sympify(g_1)
        gcd_f1g1 = sp.gcd(expr_f1, expr_g1)
        
        c_f_sym = sp.sympify(c_f)
        c_g_sym = sp.sympify(c_g)
        gcd_c = sp.gcd(c_f_sym, c_g_sym)
        
        product = sp.expand(gcd_c * gcd_f1g1)
        gcd_fg_exp = sp.expand(gcd_fg)
        
        poly_f = sp.Poly(f)
        domain = poly_f.domain
        
        neg_q = not are_associate(gcd_fg_exp, product, domain)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a UFD",
    "H_2: f and g are non-zero polynomials",
    "H_3: c_f and c_g are contents",
    "not Q: gcd is not product of gcds"
]

N_HYP = 3
NEG_Q_INDEX = 3