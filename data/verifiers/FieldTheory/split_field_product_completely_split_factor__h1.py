import sympy
from sympy import Symbol, Poly, roots, degree, Rational, Integer, sqrt, I
from sympy.abc import x, y, z
from sympy.polys.numberfields import primitive_element

def get_variable(f, g):
    free_symbols = set()
    if hasattr(f, 'free_symbols'):
        free_symbols.update(f.free_symbols)
    if hasattr(g, 'free_symbols'):
        free_symbols.update(g.free_symbols)
    if len(free_symbols) == 1:
        return list(free_symbols)[0]
    return x

def get_field_degree(gens):
    filtered_gens = []
    for g in gens:
        if g == 0:
            continue
        if hasattr(g, 'is_Rational') and g.is_Rational:
            continue
        try:
            if Rational(g) == g:
                continue
        except Exception:
            pass
        filtered_gens.append(g)
        
    unique_gens = []
    for g in filtered_gens:
        if g not in unique_gens:
            unique_gens.append(g)
            
    if not unique_gens:
        return 1
        
    var_y = Symbol('y')
    try:
        minpoly, _ = primitive_element(unique_gens, var_y)
        return degree(minpoly, var_y)
    except Exception:
        return None

def is_subfield(gensA, gensB):
    degB = get_field_degree(gensB)
    deg_union = get_field_degree(list(gensB) + list(gensA))
    if degB is None or deg_union is None:
        return False
    return degB == deg_union

def fields_equal(gensA, gensB):
    degA = get_field_degree(gensA)
    degB = get_field_degree(gensB)
    deg_union = get_field_degree(list(gensA) + list(gensB))
    if degA is None or degB is None or deg_union is None:
        return False
    return degA == degB == deg_union

def get_roots(p, var):
    if p == 0:
        return []
    poly = Poly(p, var)
    if poly.degree() == 0:
        return []
    rts = roots(p, var)
    if sum(rts.values()) != poly.degree():
        raise ValueError("Could not find all roots")
    return list(rts.keys())

def coeffs_in_field(p, var, F_gens):
    if p == 0:
        return True
    poly = Poly(p, var)
    for c in poly.coeffs():
        if not is_subfield([c], F_gens):
            return False
    return True

def is_splitting_field(p, var, F_gens, K_gens):
    if p == 0:
        return fields_equal(K_gens, F_gens)
    rts = get_roots(p, var)
    if not is_subfield(rts, K_gens):
        return False
    return fields_equal(K_gens, list(F_gens) + rts)

def splits_completely(p, var, K_gens):
    if p == 0:
        return True
    rts = get_roots(p, var)
    return is_subfield(rts, K_gens)

def neg_q_check(f, g, var, F_gens, K_gens):
    fg = f * g
    return not is_splitting_field(fg, var, F_gens, K_gens)

def conditions(witness):
    try:
        f = witness.get('f', 0)
        g = witness.get('g', 0)
        F_gens = witness.get('F_gens', [])
        K_gens = witness.get('K_gens', [])
        
        var = get_variable(f, g)
        
        try:
            h1 = coeffs_in_field(f, var, F_gens) and coeffs_in_field(g, var, F_gens)
        except Exception:
            h1 = False
            
        try:
            h2 = is_splitting_field(f, var, F_gens, K_gens)
        except Exception:
            h2 = False
            
        try:
            h3 = splits_completely(g, var, K_gens)
        except Exception:
            h3 = False
            
        try:
            neg_q = neg_q_check(f, g, var, F_gens, K_gens)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f and g are polynomials over F",
    "H_2: K is the splitting field of f over F",
    "H_3: g splits completely into linear factors over K",
    "neg_Q: K is not the splitting field of fg over F"
]

N_HYP = 3
NEG_Q_INDEX = 3