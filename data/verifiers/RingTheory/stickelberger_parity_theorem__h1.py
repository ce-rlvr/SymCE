import sympy

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                q, f_expr = witness
                n_given = None
                r_given = None
            elif len(witness) == 4:
                q, f_expr, n_given, r_given = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    h1_ok = False
    try:
        if isinstance(q, int) and sympy.isprime(q):
            domain = sympy.GF(q)
            f_poly = sympy.Poly(f_expr, x, domain=domain)
            if f_poly.is_monic:
                n_actual = f_poly.degree()
                if n_given is None or n_given == n_actual:
                    h1_ok = True
    except Exception:
        pass

    h2_ok = False
    try:
        if h1_ok:
            domain = sympy.GF(q)
            f_poly = sympy.Poly(f_expr, x, domain=domain)
            f_deriv = f_poly.diff()
            gcd_poly = f_poly.gcd(f_deriv)
            if gcd_poly.degree() == 0:
                h2_ok = True
    except Exception:
        pass

    h3_ok = False
    try:
        if h1_ok:
            if r_given is None:
                h3_ok = True
            else:
                domain = sympy.GF(q)
                f_poly = sympy.Poly(f_expr, x, domain=domain)
                factors = f_poly.factor_list()
                r_actual = sum(mult for f, mult in factors[1])
                if r_given == r_actual:
                    h3_ok = True
    except Exception:
        pass

    neg_q_ok = False
    try:
        if h1_ok:
            domain = sympy.GF(q)
            f_poly = sympy.Poly(f_expr, x, domain=domain)
            n = f_poly.degree()
            factors = f_poly.factor_list()
            r = sum(mult for f, mult in factors[1])
            
            lhs = (n % 2) == (r % 2)
            
            disc = f_poly.discriminant()
            if hasattr(disc, 'val'):
                disc_val = int(disc.val) % q
            else:
                disc_val = int(disc) % q
                
            is_nonzero_square = False
            if disc_val != 0:
                for s in range(q):
                    if (s * s) % q == disc_val:
                        is_nonzero_square = True
                        break
            
            rhs = is_nonzero_square
            
            neg_q_ok = (lhs != rhs)
    except Exception:
        pass

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: monic", "H_2: distinct roots", "H_3: r is factors", "¬Q: fails"]
N_HYP = 3
NEG_Q_INDEX = 3