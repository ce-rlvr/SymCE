import sympy
from sympy import groebner, reduced, expand, Dummy
from sympy.abc import x, y, z

# Top-level setup
# We use polynomial rings over Q. The witness should be a tuple of two lists of polynomials in x, y, z.
# These lists represent the generators of the ideals I and J respectively.
# Example witness: ([x], [y])

def is_poly_list(gens):
    if not isinstance(gens, (list, tuple)): 
        return False
    for p in gens:
        if not isinstance(p, (sympy.Expr, int)): 
            return False
        if isinstance(p, sympy.Expr):
            if not p.free_symbols.issubset({x, y, z}):
                return False
        try:
            sympy.Poly(p, x, y, z)
        except Exception:
            return False
    return True

def get_groebner(gens, *vars, **kwargs):
    gens = [p for p in gens if p != 0]
    if not gens:
        return [sympy.Integer(0)]
    gb = groebner(gens, *vars, **kwargs)
    return list(gb)

def ideal_intersection(gensA, gensB):
    if not gensA or not gensB:
        return [sympy.Integer(0)]
    t_dummy = Dummy('t')
    gens_intersect = [t_dummy * p for p in gensA] + [(1 - t_dummy) * p for p in gensB]
    gb = get_groebner(gens_intersect, t_dummy, x, y, z, order='lex')
    res = []
    for p in gb:
        if not p.has(t_dummy):
            res.append(p)
    if not res:
        return [sympy.Integer(0)]
    return res

def ideal_product(gensA, gensB):
    if not gensA or not gensB:
        return [sympy.Integer(0)]
    return [expand(p * q) for p in gensA for q in gensB]

def ideal_sum(gensA, gensB):
    return list(gensA) + list(gensB)

def ideal_equal(gensA, gensB):
    try:
        gbA = get_groebner(gensA, x, y, z)
        gbB = get_groebner(gensB, x, y, z)
        if gbA == [sympy.Integer(0)] and gbB == [sympy.Integer(0)]:
            return True
        if gbA == [sympy.Integer(0)] or gbB == [sympy.Integer(0)]:
            return False
        
        for p in gbA:
            _, rem = reduced(p, gbB, (x, y, z))
            if rem != 0: 
                return False
        for p in gbB:
            _, rem = reduced(p, gbA, (x, y, z))
            if rem != 0: 
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        I_gens, J_gens = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_poly_list(I_gens)
    except Exception:
        h1 = False

    try:
        h2 = is_poly_list(J_gens)
    except Exception:
        h2 = False

    try:
        sum_IJ = ideal_sum(I_gens, J_gens)
        int_IJ = ideal_intersection(I_gens, J_gens)
        prod_sum_int = ideal_product(sum_IJ, int_IJ)
        prod_IJ = ideal_product(I_gens, J_gens)
        
        neg_q = not ideal_equal(prod_sum_int, prod_IJ)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: (I+J)(I \\cap J) != IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2