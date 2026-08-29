import sympy
from sympy import Symbol, Poly

x = Symbol('x')

def conditions(witness):
    """
    Check if the witness satisfies the hypotheses and fails the conclusion.
    """
    try:
        f_poly = Poly(witness, x)
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field of characteristic not equal to 2 or 3
    try:
        domain = f_poly.domain
        if domain.is_Ring and not domain.is_Field:
            field_domain = domain.get_field()
        else:
            field_domain = domain
        char = field_domain.char
        h1 = (char != 2) and (char != 3) and (f_poly.degree() == 4)
    except Exception:
        h1 = False

    # H_2: The resolvent cubic of f(x) splits completely into linear factors over F
    try:
        if f_poly.degree() != 4:
            h2 = False
        else:
            coeffs = f_poly.all_coeffs()
            c4, c3, c2, c1, c0 = [f_poly.domain.to_sympy(c) for c in coeffs]
            a = c3 / c4
            b = c2 / c4
            c = c1 / c4
            d = c0 / c4
            
            y = Symbol('y')
            R_expr = y**3 - b*y**2 + (a*c - 4*d)*y - a**2*d + 4*b*d - c**2
            R_poly = Poly(R_expr, y, domain=field_domain)
            factors = R_poly.factor_list()[1]
            h2 = all(p.degree() == 1 for p, m in factors)
    except Exception:
        h2 = False

    # H_3: E is the splitting field of f(x) over F
    # This is a definitional hypothesis; it holds as long as f(x) is a valid quartic.
    try:
        h3 = f_poly.degree() == 4
    except Exception:
        h3 = False

    # ¬Q: The Galois group Gal(E/F) is NOT isomorphic to the Klein four-group V_4
    try:
        if f_poly.degree() != 4:
            neg_q = False
        else:
            if field_domain.is_FiniteField:
                # The Galois group over a finite field is cyclic, so it cannot be V_4
                neg_q = True
            else:
                if not field_domain.is_RationalField:
                    try:
                        f_poly_field = f_poly.set_domain('QQ')
                        check_domain = f_poly_field.domain
                    except Exception:
                        check_domain = None
                else:
                    f_poly_field = f_poly
                    check_domain = field_domain
                
                if check_domain is None:
                    neg_q = False
                else:
                    factors = f_poly_field.factor_list()[1]
                    unique_factors = [p for p, m in factors]
                    degrees = [p.degree() for p in unique_factors]
                    
                    max_deg = max(degrees)
                    if max_deg == 1:
                        is_v4 = False
                    elif max_deg == 4:
                        # For an irreducible quartic, Gal is V_4 iff the resolvent cubic splits completely
                        is_v4 = h2
                    elif max_deg == 3:
                        is_v4 = False
                    elif max_deg == 2:
                        quadratics = [p for p in unique_factors if p.degree() == 2]
                        if len(quadratics) == 1:
                            is_v4 = False
                        elif len(quadratics) == 2:
                            q1, q2 = quadratics
                            c1_list = [q1.domain.to_sympy(c) for c in q1.all_coeffs()]
                            c2_list = [q2.domain.to_sympy(c) for c in q2.all_coeffs()]
                            a1, b1, c1 = c1_list
                            a2, b2, c2 = c2_list
                            D1 = b1**2 - 4*a1*c1
                            D2 = b2**2 - 4*a2*c2
                            # They generate the same field iff D1/D2 is a rational square
                            if sympy.sqrt(D1 / D2).is_rational:
                                is_v4 = False
                            else:
                                is_v4 = True
                        else:
                            is_v4 = False
                    else:
                        is_v4 = False
                        
                    neg_q = not is_v4
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2 or 3",
    "H_2: The resolvent cubic of f(x) splits completely into linear factors over F",
    "H_3: E is the splitting field of f(x) over F",
    "¬Q: The Galois group Gal(E/F) is NOT isomorphic to the Klein four-group V_4"
]

N_HYP = 3
NEG_Q_INDEX = 3