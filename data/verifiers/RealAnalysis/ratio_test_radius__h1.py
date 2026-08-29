import sympy
from sympy import Symbol, Abs, limit, oo

CONDITION_LABELS = [
    "H_1: a_n != 0 for all sufficiently large n",
    "H_2: limit L = lim |a_{n+1}/a_n| exists in R U {oo}",
    "¬Q: The radius of convergence of the power series is NOT 1/L"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n = Symbol('n', integer=True, positive=True)
    x = Symbol('x', real=True)
    
    a_n = None
    term = None
    
    if isinstance(witness, tuple) and len(witness) == 2:
        a_n, term = witness
        vars_list = [s for s in getattr(term, 'free_symbols', []) if s.name != 'n']
        var = vars_list[0] if vars_list else x
    else:
        if isinstance(witness, sympy.Sum):
            term = witness.args[0]
        else:
            term = witness
        vars_list = [s for s in getattr(term, 'free_symbols', []) if s.name != 'n']
        var = vars_list[0] if vars_list else x

    if term is None:
        return [False, False, False]

    k_n_expr = sympy.Integer(1)
    x_0_val = sympy.Integer(0)
    C_n = term

    if term.has(var):
        try:
            d_term = sympy.diff(term, var)
            if d_term != 0:
                ratio_expr = sympy.simplify(term / d_term)
                d_ratio = sympy.diff(ratio_expr, var)
                if d_ratio != 0:
                    k_n_expr = sympy.simplify(1 / d_ratio)
                    x_0 = sympy.simplify(var - k_n_expr * ratio_expr)
                    if x_0.has(var):
                        x_0_val = limit(x_0, var, 1)
                    else:
                        x_0_val = x_0
            C_n = sympy.simplify(term.subs(var, x_0_val + 1))
        except Exception:
            C_n = term.subs(var, 1)
            
    if a_n is None:
        a_n = C_n

    # H1: a_n != 0 for all sufficiently large n
    try:
        h1 = bool(sympy.simplify(a_n) != 0)
    except Exception:
        h1 = False
        
    # H2: limit L exists
    try:
        ratio = sympy.simplify(Abs(a_n.subs(n, n+1) / a_n))
        L = limit(ratio, n, oo)
        if hasattr(L, 'has') and L.has(sympy.AccumBounds):
            h2 = False
        else:
            h2 = bool(L.is_real or L == oo)
    except Exception:
        h2 = False
        
    # neg_Q: R != 1/L
    try:
        if L == 0:
            inv_L = oo
        elif L == oo:
            inv_L = 0
        else:
            inv_L = 1 / L
            
        if not term.has(var):
            neg_q = False
        else:
            if k_n_expr.has(var):
                k_n = limit(k_n_expr, var, 1)
            else:
                k_n = k_n_expr
                
            R_actual = limit(Abs(C_n)**(-1/k_n), n, oo)
            
            if hasattr(R_actual, 'has') and R_actual.has(sympy.AccumBounds):
                R_actual = R_actual.min
                
            if isinstance(R_actual, sympy.Limit) or (hasattr(R_actual, 'has') and R_actual.has(sympy.Limit)):
                # Fallback
                c = limit(k_n / n, n, oo)
                L_C = limit(Abs(C_n.subs(n, n+1) / C_n), n, oo)
                if hasattr(L_C, 'has') and L_C.has(sympy.AccumBounds):
                    L_C = L_C.max
                    
                if L_C == 1:
                    R_actual = sympy.Integer(1)
                elif L_C == 0:
                    R_actual = oo
                elif L_C == oo:
                    R_actual = sympy.Integer(0)
                else:
                    R_actual = (1/L_C)**(1/c)
                    
            if R_actual == inv_L:
                neg_q = False
            else:
                diff = sympy.simplify(R_actual - inv_L)
                neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]