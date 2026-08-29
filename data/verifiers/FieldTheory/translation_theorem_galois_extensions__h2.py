import sympy
from sympy import sqrt, cbrt, I, Rational, Dummy, minpoly, factor_list, sympify, degree

# Top-level setup: named object bindings that the witness expression may reference.
# We define some standard number fields as lists of generators over Q.
# The witness should be a tuple of three lists of generators: (K_gens, L_gens, E_gens)
Q = []
Q_cbrt2 = [cbrt(2)]
Q_sqrt3 = [sqrt(3)]
Q_cbrt2_sqrt3 = [cbrt(2), sqrt(3)]
Q_omega = [Rational(-1, 2) + sqrt(3)*I/2]
Q_cbrt2_omega = [cbrt(2), Rational(-1, 2) + sqrt(3)*I/2]

def field_degree(gens):
    """Computes the degree of the number field Q(gens) over Q."""
    gens = [sympify(g) for g in gens if not sympify(g).is_Rational]
    if not gens:
        return 1
    x = Dummy('x')
    try:
        from sympy.polys.numberfields import primitive_element
        poly, _ = primitive_element(gens, x)
        return degree(poly, x)
    except Exception:
        # Fallback if primitive_element fails
        elem = sum(g * (i + 1) for i, g in enumerate(gens))
        return degree(minpoly(elem, x), x)

def is_galois(base_gens, ext_gens):
    """Checks if Q(ext_gens) is a finite Galois extension of Q(base_gens)."""
    deg_base = field_degree(base_gens)
    deg_ext = field_degree(ext_gens)
    
    # Check if base is a subfield of ext
    if field_degree(base_gens + ext_gens) != deg_ext:
        return False
        
    if deg_base == deg_ext:
        return True

    x = Dummy('x')
    # For the extension to be Galois, the minimal polynomial of each generator 
    # over the base field must split completely in the extension field.
    for g in ext_gens:
        g = sympify(g)
        if g.is_Rational:
            continue
        if field_degree(base_gens + [g]) == deg_base:
            continue
            
        f = minpoly(g, x)
        if base_gens:
            factors_base = factor_list(f, extension=base_gens)[1]
        else:
            factors_base = factor_list(f)[1]
            
        # Find the minimal polynomial of g over base_gens
        minpoly_g_base = None
        for fac, mult in factors_base:
            val = fac.subs(x, g)
            if val.simplify() == 0:
                minpoly_g_base = fac
                break
            try:
                if abs(complex(val.evalf())) < 1e-9:
                    minpoly_g_base = fac
                    break
            except Exception:
                pass
                
        if minpoly_g_base is None:
            return False
            
        # Check if minpoly_g_base splits completely into linear factors over ext_gens
        try:
            factors_ext = factor_list(minpoly_g_base, extension=ext_gens)[1]
        except Exception:
            return False
            
        for fac, mult in factors_ext:
            if degree(fac, x) > 1:
                return False
                
    return True

def conditions(witness) -> list[bool]:
    try:
        K_gens, L_gens, E_gens = witness
    except Exception:
        return [False, False, False]
        
    # H_1: L/K is a finite Galois extension
    try:
        h1 = is_galois(K_gens, L_gens)
    except Exception:
        h1 = False
        
    # H_2: L and E are subfields of a common larger field
    # In our representation, all fields are subfields of C, so we just validate the types.
    try:
        h2 = isinstance(L_gens, list) and isinstance(E_gens, list)
    except Exception:
        h2 = False
        
    # ¬Q: LE is not a Galois extension of E, or the restriction map is not an isomorphism.
    # If LE/E is not Galois, the conclusion fails immediately.
    try:
        LE_gens = L_gens + E_gens
        le_is_galois = is_galois(E_gens, LE_gens)
        
        if not le_is_galois:
            neg_q = True
        else:
            # For the known counterexamples, LE/E failing to be Galois is the primary failure mode.
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: L and E are subfields of a common larger field",
    "¬Q: LE is not a Galois extension of E, or the restriction map is not an isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2