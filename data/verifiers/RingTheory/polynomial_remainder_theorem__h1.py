import sympy as sp

A = sp.Symbol('A', commutative=False)
B = sp.Symbol('B', commutative=False)
C = sp.Symbol('C', commutative=False)
x = sp.Symbol('x', commutative=True)

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        f_expr, x_sym, c_val = witness
        f_expr = sp.sympify(f_expr)
        x_sym = sp.sympify(x_sym)
        c_val = sp.sympify(c_val)
    except Exception:
        return [False, False, False]
    
    try:
        expr_expanded = f_expr.expand()
        terms = expr_expanded.as_ordered_terms() if expr_expanded.is_Add else [expr_expanded]
        is_poly = True
        for term in terms:
            indep, dep = term.as_independent(x_sym)
            if dep == 1 or dep == x_sym:
                continue
            if dep.is_Pow and dep.base == x_sym and dep.exp.is_Integer and dep.exp >= 0:
                continue
            is_poly = False
            break
        h1 = bool(is_poly)
    except Exception:
        h1 = False

    try:
        h2 = bool(not c_val.has(x_sym))
    except Exception:
        h2 = False

    try:
        f_c = f_expr.subs(x_sym, c_val).expand()
        
        rem_right = 0
        rem_left = 0
        for term in terms:
            indep, dep = term.as_independent(x_sym)
            if dep == 1:
                rem_right += indep
                rem_left += indep
            elif dep == x_sym:
                rem_right += indep * c_val
                rem_left += c_val * indep
            elif dep.is_Pow and dep.base == x_sym and dep.exp.is_Integer and dep.exp >= 0:
                rem_right += indep * (c_val ** dep.exp)
                rem_left += (c_val ** dep.exp) * indep
                
        rem_right = rem_right.expand()
        rem_left = rem_left.expand()
        
        diff_right = (f_c - rem_right).expand()
        diff_left = (f_c - rem_left).expand()
        
        neg_q = bool((diff_right != 0) and (diff_left != 0))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over F",
    "H_2: c is an element of F",
    "¬Q: The remainder when f(x) is divided by (x - c) is not f(c)"
]

N_HYP = 2
NEG_Q_INDEX = 2