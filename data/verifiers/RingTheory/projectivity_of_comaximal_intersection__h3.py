import sympy
from sympy import symbols, sympify, groebner, reduced, Poly, div
import math
import itertools
import functools

# Top-level setup
# We define standard symbols that might be used, though the witness 
# is expected to provide its own variable names.
x, y, z, w = symbols('x y z w')

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: I and J are projective as R-modules",
    "¬Q: The intersection I \\cap J is not a projective R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3

def ideal_intersection(A_gens, B_gens, vars):
    if not A_gens or not B_gens:
        return [0]
    t = symbols('t_intersect')
    all_vars = (t,) + vars
    gens = [t * a for a in A_gens] + [(1 - t) * b for b in B_gens]
    gens = [g for g in gens if g != 0]
    if not gens:
        return [0]
    gb = groebner(gens, *all_vars, order='lex')
    intersect_gens = []
    for p in gb:
        if t not in p.free_symbols:
            intersect_gens.append(p)
    if not intersect_gens:
        return [0]
    return intersect_gens

def ideal_quotient_principal(A_gens, b, vars):
    if b == 0:
        return [1]
    if not A_gens:
        return [0]
    intersect_gens = ideal_intersection(A_gens, [b], vars)
    quot_gens = []
    for p in intersect_gens:
        if p == 0:
            continue
        q, r = div(p, b, *vars, domain='QQ')
        if r == 0:
            quot_gens.append(q)
        else:
            try:
                q = Poly(p, *vars).exquo(Poly(b, *vars)).as_expr()
                quot_gens.append(q)
            except Exception:
                pass
    if not quot_gens:
        return [0]
    return quot_gens

def ideal_quotient(A_gens, B_gens, vars):
    if not B_gens:
        return [1]
    res = ideal_quotient_principal(A_gens, B_gens[0], vars)
    for b in B_gens[1:]:
        q_b = ideal_quotient_principal(A_gens, b, vars)
        res = ideal_intersection(res, q_b, vars)
    return res

def is_projective(I_gens, K_gens, vars):
    """
    Checks if an ideal I is projective in the domain R = Q[vars]/K.
    For a domain, an ideal is projective iff it is invertible,
    which is equivalent to d \in I * (d R : I) for any non-zero d \in I.
    """
    I_prime = I_gens + K_gens
    
    if not K_gens:
        gb_K = []
    else:
        gb_K = groebner(K_gens, *vars)
        
    is_zero = True
    for g in I_gens:
        if not K_gens:
            rem = g
        else:
            rem = reduced(g, gb_K, *vars)[1]
        if rem != 0:
            is_zero = False
            break
    if is_zero:
        return True
        
    d = None
    for g in I_gens:
        if not K_gens:
            rem = g
        else:
            rem = reduced(g, gb_K, *vars)[1]
        if rem != 0:
            d = g
            break
            
    A_gens = [d] + K_gens
    Q_prime = ideal_quotient(A_gens, I_prime, vars)
    
    IQ_K_gens = list(K_gens)
    for i in I_prime:
        for q in Q_prime:
            IQ_K_gens.append(i * q)
            
    IQ_K_gens = [g for g in IQ_K_gens if g != 0]
    if not IQ_K_gens:
        rem = d
    else:
        gb_IQ_K = groebner(IQ_K_gens, *vars)
        rem = reduced(d, gb_IQ_K, *vars)[1]
        
    return rem == 0

def conditions(witness):
    """
    Expects witness in the format: (var_names, K_strs, I_strs, J_strs)
    Example: (['x', 'y', 'z', 'w'], ['x*y - z*w'], ['x'], ['z'])
    representing R = Q[x,y,z,w]/(xy - zw), I = (x), J = (z).
    """
    try:
        var_names, K_strs, I_strs, J_strs = witness
        
        vars_tuple = tuple(symbols(v) for v in var_names)
        local_dict = {name: v for name, v in zip(var_names, vars_tuple)}
        
        K_gens = [sympify(g, locals=local_dict) for g in K_strs]
        I_gens = [sympify(g, locals=local_dict) for g in I_strs]
        J_gens = [sympify(g, locals=local_dict) for g in J_strs]
        
        def is_poly(gens):
            return all(g.free_symbols.issubset(set(vars_tuple)) for g in gens)
        
        # H1: R is a commutative ring (always true for polynomial quotients)
        h1 = is_poly(K_gens)
        
        # H2: I and J are ideals of R (given by generators)
        h2 = is_poly(I_gens) and is_poly(J_gens)
        
        # H3: I and J are projective as R-modules
        h3 = is_projective(I_gens, K_gens, vars_tuple) and is_projective(J_gens, K_gens, vars_tuple)
        
        # ¬Q: I \cap J is NOT projective
        I_prime = I_gens + K_gens
        J_prime = J_gens + K_gens
        intersect_gens = ideal_intersection(I_prime, J_prime, vars_tuple)
        
        neg_q = not is_projective(intersect_gens, K_gens, vars_tuple)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]