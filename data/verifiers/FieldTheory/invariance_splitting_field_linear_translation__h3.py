import sympy
from sympy import *
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

def field_degree(gens):
    clean_gens = []
    for g in gens:
        g = sympify(g)
        if g.is_Rational:
            continue
        if g not in clean_gens:
            clean_gens.append(g)
    if not clean_gens:
        return 1
    try:
        minpoly, _ = primitive_element(clean_gens, x, polys=True)
        return minpoly.degree()
    except Exception:
        return None

def is_in_field(expr, gens):
    try:
        expr = sympify(expr)
        if expr.is_Rational:
            return True
        d1 = field_degree(gens)
        d2 = field_degree(gens + [expr])
        return d1 is not None and d1 == d2
    except Exception:
        return False

def is_poly_in_field(f, gens):
    try:
        poly = Poly(f, x)
        for coeff in poly.coeffs():
            if not is_in_field(coeff, gens):
                return False
        return True
    except Exception:
        return False

def is_splitting_field(E_gens, f, F_gens):
    try:
        poly = Poly(f, x)
        rts = roots(f, x)
        if sum(rts.values()) != poly.degree():
            return False
        
        roots_list = list(rts.keys())
        d_F_E = field_degree(F_gens + E_gens)
        d_F_roots = field_degree(F_gens + roots_list)
        d_both = field_degree(F_gens + E_gens + roots_list)
        
        if d_F_E is None or d_F_roots is None or d_both is None:
            return False
            
        return d_F_E == d_F_roots and d_F_E == d_both
    except Exception:
        return False

def conditions(witness):
    """
    witness is expected to be a dictionary with keys:
      'F_gens': list of generators for F over QQ
      'f': polynomial expression in x
      'c': expression for the translation constant
      'g': polynomial expression in x
      'E1_gens': list of generators for E_1 over QQ
      'E2_gens': list of generators for E_2 over QQ
    """
    try:
        F_gens = witness.get('F_gens', [])
        if 'f' not in witness or 'c' not in witness or 'g' not in witness:
            return [False] * 6
        f = sympify(witness['f'])
        c = sympify(witness['c'])
        g = sympify(witness['g'])
        E1_gens = witness.get('E1_gens', [])
        E2_gens = witness.get('E2_gens', [])
    except Exception:
        return [False] * 6

    # H_1: F is a field (represented by its generators over QQ)
    h1 = isinstance(F_gens, list)

    # H_2: f is a polynomial over F
    try:
        h2 = is_poly_in_field(f, F_gens)
    except Exception:
        h2 = False

    # H_3: g is f translated by c
    try:
        expected_g = f.subs(x, x - c).expand()
        actual_g = g.expand()
        h3 = simplify(expected_g - actual_g) == 0
    except Exception:
        h3 = False

    # H_4: E_1 is a splitting field of f over F
    try:
        h4 = is_splitting_field(E1_gens, f, F_gens)
    except Exception:
        h4 = False

    # H_5: E_2 is a splitting field of g over F
    try:
        h5 = is_splitting_field(E2_gens, g, F_gens)
    except Exception:
        h5 = False

    # ¬Q: E_1 and E_2 are NOT isomorphic over F
    # For splitting fields (normal extensions), they are isomorphic over F iff they are equal.
    try:
        d_E1 = field_degree(F_gens + E1_gens)
        d_E2 = field_degree(F_gens + E2_gens)
        d_both = field_degree(F_gens + E1_gens + E2_gens)
        
        isomorphic = (d_E1 is not None) and (d_E1 == d_E2) and (d_E1 == d_both)
        neg_q = not isomorphic
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: g is f translated by c",
    "H_4: E_1 is a splitting field of f over F",
    "H_5: E_2 is a splitting field of g over F",
    "not Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 5
NEG_Q_INDEX = 5