import sympy as sp
from sympy.abc import x, y, z, t, u, v, w

# Top-level setup
# The witness should be a tuple: (vars_list, I_list, x_elem) or (I_list, x_elem)
# where I_list is a list of lists of polynomials (generators for each I_k), 
# and x_elem is a polynomial representing x.
# The ring R is taken to be the polynomial ring over QQ in the given variables.

def is_in_ideal(p, I_gens, vars_list):
    I_gens = [g for g in I_gens if g != 0]
    if not I_gens:
        return sp.expand(p) == 0
    gb = sp.groebner(I_gens, *vars_list, domain='QQ')
    Q, r = sp.reduced(p, gb, *vars_list, domain='QQ')
    return r == 0

def intersect_ideals(I1_gens, I2_gens, vars_list):
    I1_gens = [g for g in I1_gens if g != 0]
    I2_gens = [g for g in I2_gens if g != 0]
    if not I1_gens or not I2_gens:
        return []
    t_dummy = sp.Symbol('t_intersect_dummy')
    all_vars = [t_dummy] + list(vars_list)
    gens = [t_dummy * g for g in I1_gens] + [(1 - t_dummy) * g for g in I2_gens]
    gb = sp.groebner(gens, *all_vars, order='lex', domain='QQ')
    intersect_gens = []
    for p in gb:
        expr = p.as_expr() if hasattr(p, 'as_expr') else sp.sympify(p)
        if not expr.has(t_dummy):
            intersect_gens.append(expr)
    return intersect_gens

def ideal_quotient(I_gens, x_elem, vars_list):
    intersect_gens = intersect_ideals(I_gens, [x_elem], vars_list)
    quotient_gens = []
    for g in intersect_gens:
        q, r = sp.div(g, x_elem, *vars_list, domain='QQ')
        quotient_gens.append(q)
    return quotient_gens

def is_zero_divisor_or_zero(x_elem, I_gens, vars_list):
    if is_in_ideal(x_elem, I_gens, vars_list):
        return True
    
    quotient_gens = ideal_quotient(I_gens, x_elem, vars_list)
    for g in quotient_gens:
        if not is_in_ideal(g, I_gens, vars_list):
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            vars_list, I_list, x_elem = witness
        elif len(witness) == 2:
            I_list, x_elem = witness
            vars_list = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        normalized_I_list = []
        for I in I_list:
            if hasattr(I, 'gens'):
                normalized_I_list.append(list(I.gens))
            else:
                normalized_I_list.append(list(I))
                
        if vars_list is None:
            symbols = set()
            if isinstance(x_elem, sp.Expr):
                symbols.update(x_elem.free_symbols)
            for gens in normalized_I_list:
                for g in gens:
                    if isinstance(g, sp.Expr):
                        symbols.update(g.free_symbols)
            vars_list = sorted(list(symbols), key=lambda s: s.name)
            
        if not vars_list:
            vars_list = [sp.Symbol('dummy_var')]
            
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring (Polynomial ring over QQ is commutative)
    h1 = True
    
    # H2: I = \bigcap_{k=1}^n I_k
    try:
        h2 = isinstance(normalized_I_list, list) and len(normalized_I_list) > 0
    except Exception:
        h2 = False
        
    # H3: x \in R
    try:
        h3 = isinstance(x_elem, (sp.Expr, int, float))
    except Exception:
        h3 = False
        
    if not (h1 and h2 and h3):
        return [h1, h2, h3, False]
        
    try:
        # Compute I = \bigcap I_k
        I_gens = normalized_I_list[0]
        for i in range(1, len(normalized_I_list)):
            I_gens = intersect_ideals(I_gens, normalized_I_list[i], vars_list)
            
        # Check if x is a zero divisor or zero in R/I
        lhs = is_zero_divisor_or_zero(x_elem, I_gens, vars_list)
        
        # Check if there exists k such that x is a zero divisor or zero in R/I_k
        rhs = False
        for gens in normalized_I_list:
            if is_zero_divisor_or_zero(x_elem, gens, vars_list):
                rhs = True
                break
                
        # The conclusion fails if the equivalence does not hold
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I = \\bigcap_{k=1}^n I_k",
    "H_3: x \\in R",
    "¬Q: The equivalence between x being a zero divisor/zero in R/I and in some R/I_k does not hold"
]

N_HYP = 3
NEG_Q_INDEX = 3