import sympy

# Top-level setup
x = sympy.Symbol('x')

def is_poly_over_Q(witness):
    try:
        if not isinstance(witness, sympy.Expr):
            return False
        free_syms = witness.free_symbols
        if len(free_syms) > 1:
            return False
        
        sym = list(free_syms)[0] if free_syms else x
        poly = sympy.Poly(witness, sym)
        return poly.domain.is_QQ or poly.domain.is_ZZ
    except Exception:
        return False

def is_S4_galois_group(poly_expr):
    try:
        free_syms = poly_expr.free_symbols
        sym = list(free_syms)[0] if free_syms else x
        poly = sympy.Poly(poly_expr, sym)
        if not (poly.domain.is_QQ or poly.domain.is_ZZ):
            return False
            
        # Factor the polynomial over Q
        factors = [f[0] for f in sympy.factor_list(poly)[1]]
        
        has_S4_factor = False
        S4_factor = None
        for f in factors:
            if f.degree() == 4:
                # Check discriminant
                disc = f.discriminant()
                if sympy.sqrt(disc).is_rational:
                    continue
                
                # Check resolvent cubic for irreducibility
                coeffs = f.all_coeffs()
                lead = coeffs[0]
                a = coeffs[1]/lead
                b = coeffs[2]/lead
                c = coeffs[3]/lead
                d = coeffs[4]/lead
                
                res_cubic = sym**3 - b*sym**2 + (a*c - 4*d)*sym - a**2*d + 4*b*d - c**2
                if sympy.Poly(res_cubic, sym).is_irreducible:
                    has_S4_factor = True
                    S4_factor = f
                    break
                    
        if has_S4_factor:
            # If the polynomial has an S4 factor, the overall Galois group is S4 
            # if all other factors are linear (their splitting fields are trivial).
            if all(f.degree() == 1 for f in factors if f != S4_factor):
                return True
                
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    h1 = is_poly_over_Q(witness)
    
    if not h1:
        return [False, False]
        
    try:
        # The conclusion is that the Galois group is S4 (and degree is 24).
        # The negated conclusion is True if the Galois group is NOT S4.
        neg_q = not is_S4_galois_group(witness)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "¬Q: The degree of the extension is not 24, or the Galois group is not isomorphic to S4"
]

N_HYP = 1
NEG_Q_INDEX = 1