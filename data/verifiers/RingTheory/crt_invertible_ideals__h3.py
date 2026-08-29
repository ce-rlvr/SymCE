import sympy
from sympy.abc import x, y, z, w, a, b, c, d, t

def get_gb(gens, vars_list):
    gens = [g for g in gens if g != 0]
    if not gens:
        return []
    gb = sympy.groebner(gens, *vars_list, domain='QQ')
    return [p.as_expr() for p in gb if p.as_expr() != 0]

def reduce_poly(f, gb, vars_list):
    if f == 0:
        return sympy.S.Zero
    gb = [g for g in gb if g != 0]
    if not gb:
        return sympy.expand(f)
    _, rem = sympy.reduced(f, gb, *vars_list, domain='QQ')
    return rem

def intersect_ideals(I_gens, J_gens, vars_list):
    I_gens = [g for g in I_gens if g != 0]
    J_gens = [g for g in J_gens if g != 0]
    if not I_gens or not J_gens:
        return []
    t_var = sympy.Symbol('t_intersect_dummy')
    L_gens = [t_var * f for f in I_gens] + [(1 - t_var) * g for g in J_gens]
    gb = sympy.groebner(L_gens, t_var, *vars_list, order='lex', domain='QQ')
    res = []
    for p in gb:
        expr = p.as_expr()
        if expr != 0 and t_var not in expr.free_symbols:
            res.append(expr)
    return res

def is_invertible(M_gens, K_gens, vars_list):
    M_gens = M_gens + K_gens
    m_gens = list(vars_list)
    mM_gens = [v * f for v in m_gens for f in M_gens]
    J_gens = mM_gens + K_gens
    
    J_gb = get_gb(J_gens, vars_list)
    M_gb = get_gb(M_gens, vars_list)
    
    reduced_gens = []
    for g in M_gb:
        rem = reduce_poly(g, J_gb, vars_list)
        if rem != 0:
            reduced_gens.append(rem)
            
    if not reduced_gens:
        return False
        
    monomials = set()
    polys = []
    for g in reduced_gens:
        p = sympy.Poly(g, *vars_list, domain='QQ')
        polys.append(p)
        monomials.update([term[0] for term in p.terms()])
        
    monomials = list(monomials)
    matrix_rows = []
    for p in polys:
        p_dict = dict(p.terms())
        row = [p_dict.get(mon, 0) for mon in monomials]
        matrix_rows.append(row)
        
    rank = sympy.Matrix(matrix_rows).rank()
    
    if rank != 1:
        return False
        
    f = reduced_gens[0]
    
    int_gens = intersect_ideals(K_gens, [f], vars_list)
    K_gb = get_gb(K_gens, vars_list)
    
    for g in int_gens:
        quots, r = sympy.reduced(g, [f], *vars_list, domain='QQ')
        if r != 0:
            return False
        q = quots[0]
        rem = reduce_poly(q, K_gb, vars_list)
        if rem != 0:
            return False
            
    return True

def conditions(witness):
    """
    witness format: (vars_list, K_gens, I_gens, J_gens)
    where:
      - vars_list: list of sympy symbols (e.g., [x, y, z, w])
      - K_gens: list of sympy expressions generating the relation ideal K
      - I_gens: list of sympy expressions generating ideal I
      - J_gens: list of sympy expressions generating ideal J
    The ring R is defined as Q[vars_list] / K.
    """
    try:
        vars_list, K_gens, I_gens, J_gens = witness
        
        # H1: R is a commutative ring
        # By definition of our setup, R = Q[vars]/K is a commutative ring.
        h1 = True
        
        # H2: I is an invertible ideal
        h2 = is_invertible(I_gens, K_gens, vars_list)
        
        # H3: J is an invertible ideal
        h3 = is_invertible(J_gens, K_gens, vars_list)
        
        # Conclusion: I \cap J is an invertible ideal
        M_gens = intersect_ideals(I_gens + K_gens, J_gens + K_gens, vars_list)
        q = is_invertible(M_gens, K_gens, vars_list)
        
        return [h1, h2, h3, not q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an invertible ideal of R",
    "H_3: J is an invertible ideal of R",
    "¬Q: I \\cap J is not an invertible ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3