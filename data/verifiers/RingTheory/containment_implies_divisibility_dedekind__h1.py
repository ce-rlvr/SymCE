import sympy as sp

# Top-level setup
x, y, z = sp.symbols('x y z')

def ideal_intersection(I_gens, J_gens, vars):
    t = sp.Symbol('__t_dummy_for_intersection__')
    gens = [t * g for g in I_gens] + [(1 - t) * g for g in J_gens]
    gb = sp.groebner(gens, t, *vars, domain='QQ', order='lex')
    return [g for g in gb if t not in g.free_symbols]

def ideal_quotient_principal(I_gens, f, vars):
    if f == 0:
        return [sp.S.One]
    intersect_gens = ideal_intersection(I_gens, [f], vars)
    q_gens = []
    for g in intersect_gens:
        q, r = sp.div(g, f, *vars, domain='QQ')
        if r == 0:
            q_gens.append(q)
    return q_gens

def ideal_quotient(I_gens, J_gens, vars):
    if not J_gens or all(f == 0 for f in J_gens):
        return [sp.S.One]
    result_gens = ideal_quotient_principal(I_gens, J_gens[0], vars)
    for f in J_gens[1:]:
        q_gens = ideal_quotient_principal(I_gens, f, vars)
        result_gens = ideal_intersection(result_gens, q_gens, vars)
    return result_gens

def ideal_multiply(I_gens, J_gens):
    return [f * g for f in I_gens for g in J_gens]

def ideal_equal(I_gens, J_gens, vars):
    if not I_gens: I_gens = [sp.S.Zero]
    if not J_gens: J_gens = [sp.S.Zero]
    gb_I = sp.groebner(I_gens, *vars, domain='QQ')
    gb_J = sp.groebner(J_gens, *vars, domain='QQ')
    return list(gb_I) == list(gb_J)

def ideal_subset(I_gens, J_gens, vars):
    if not I_gens: return True
    if not J_gens:
        return all(sp.sympify(f) == 0 for f in I_gens)
    gb_J = list(sp.groebner(J_gens, *vars, domain='QQ'))
    for f in I_gens:
        r = sp.reduced(f, gb_J, *vars, domain='QQ')[1]
        if r != 0:
            return False
    return True

def is_nonzero_ideal(gens, vars):
    if not gens: return False
    gb = sp.groebner(gens, *vars, domain='QQ')
    return not all(g == 0 for g in gb)

def conditions(witness) -> list[bool]:
    try:
        I_gens, J_gens = witness
    except Exception:
        return [False, False, False]
    
    try:
        I_gens = [sp.nsimplify(sp.sympify(g)) for g in I_gens]
        J_gens = [sp.nsimplify(sp.sympify(g)) for g in J_gens]
        
        symbols = set()
        for f in I_gens + J_gens:
            symbols.update(f.free_symbols)
        if not symbols:
            vars = [x]
        else:
            vars = sorted(list(symbols), key=lambda s: s.name)
            
        # H_1: I and J are non-zero ideals of R
        h1 = is_nonzero_ideal(I_gens, vars) and is_nonzero_ideal(J_gens, vars)
        
        # H_2: I is a subset of J
        h2 = ideal_subset(I_gens, J_gens, vars)
        
        # ¬Q: There does not exist an ideal K such that I = JK
        # If such K exists, then K = I : J must satisfy I = J * (I : J).
        # We compute K = I : J and check if I == JK. If not, no such K exists.
        K_gens = ideal_quotient(I_gens, J_gens, vars)
        JK_gens = ideal_multiply(J_gens, K_gens)
        neg_q = not ideal_equal(I_gens, JK_gens, vars)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I and J are non-zero ideals of R",
    "H_2: I is a subset of J",
    "¬Q: There does not exist an ideal K such that I = JK"
]

N_HYP = 2
NEG_Q_INDEX = 2