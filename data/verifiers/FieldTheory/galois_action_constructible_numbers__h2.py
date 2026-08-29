import sympy
from sympy import Poly, Rational, Integer
from sympy.abc import x

def check_h1(obj):
    """
    Check if the object represents a real constructible number.
    If it's an expression, we check its minimal polynomial.
    If it's a polynomial, we check if it has an irreducible factor of degree 1 or 2 with a real root.
    """
    try:
        if isinstance(obj, sympy.Expr) and not obj.has(x):
            if obj.is_real is not False:
                min_poly = sympy.minpoly(obj, x)
                d = sympy.degree(min_poly, x)
                if d == 1 or d == 2:
                    return True
    except Exception:
        pass
    
    try:
        f = Poly(obj, x, domain='QQ')
        factors = f.factor_list()[1]
        for g_expr, mult in factors:
            g = Poly(g_expr, x, domain='QQ')
            d = g.degree()
            if d == 1:
                return True
            if d == 2:
                coeffs = g.all_coeffs()
                # Check discriminant for real roots
                if coeffs[1]**2 - 4*coeffs[0]*coeffs[2] >= 0:
                    return True
    except Exception:
        pass
    
    return False

def check_neg_q(obj):
    """
    Check if the splitting field of the polynomial has a degree that is NOT a power of 2,
    or its Galois group is NOT a 2-group.
    """
    try:
        f = Poly(obj, x, domain='QQ')
        factors = f.factor_list()[1]
        for g_expr, mult in factors:
            g = Poly(g_expr, x, domain='QQ')
            d = g.degree()
            
            # If the degree of an irreducible factor is not a power of 2,
            # its Galois group order is divisible by an odd prime.
            if d & (d - 1) != 0:
                return True
            
            # If degree is 4, check the cubic resolvent.
            # If it has no rational root, the Galois group is A4 or S4 (not a 2-group).
            if d == 4:
                coeffs = g.all_coeffs()
                lead = coeffs[0]
                a = coeffs[1] / lead
                b = coeffs[2] / lead
                c = coeffs[3] / lead
                d_coeff = coeffs[4] / lead
                
                # Cubic resolvent: y^3 - b*y^2 + (a*c - 4*d)*y - a^2*d + 4*b*d - c^2
                res = Poly(x**3 - b*x**2 + (a*c - 4*d_coeff)*x - a**2*d_coeff + 4*b*d_coeff - c**2, x, domain='QQ')
                has_rat_root = False
                for res_factor, _ in res.factor_list()[1]:
                    if res_factor.degree() == 1:
                        has_rat_root = True
                        break
                if not has_rat_root:
                    return True
    except Exception:
        pass
    
    return False

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        # The witness could be a tuple (alpha, L_poly) or just a polynomial f(x)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            h1_ok = check_h1(witness[0])
            neg_q_ok = check_neg_q(witness[1])
        else:
            h1_ok = check_h1(witness)
            neg_q_ok = check_neg_q(witness)
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: alpha is a real number that is constructible by straightedge and compass from Q",
    "¬Q: The degree of L over Q is not a power of 2, or the Galois group is not a finite 2-group"
]

N_HYP = 1
NEG_Q_INDEX = 1