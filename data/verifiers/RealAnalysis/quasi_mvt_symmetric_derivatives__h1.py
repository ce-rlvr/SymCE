import sympy as sp
from sympy.abc import x

# Top-level setup for witness expressions
h = sp.Symbol('h', real=True)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the 
    Quasi-Mean Value Theorem for Symmetric Derivatives (without continuity).
    
    Witness should be a tuple (f_expr, a, b) or a dictionary with these keys,
    where f_expr is a sympy expression in terms of x, and a, b are real numbers.
    """
    try:
        if isinstance(witness, dict):
            f_expr = witness['f']
            a = witness['a']
            b = witness['b']
        else:
            f_expr, a, b = witness
            
        if isinstance(f_expr, str):
            f_expr = sp.sympify(f_expr)
            
        a = float(a)
        b = float(b)
        
        if a >= b:
            return [False, False]
    except Exception:
        return [False, False]
        
    h1_ok = True
    neg_q_ok = False
    
    # Try symbolic evaluation first for rigorous limits
    try:
        S = float((f_expr.subs(x, b) - f_expr.subs(x, a)) / (b - a))
        
        fs_values = []
        eval_points = [a + (b - a) * i / 50.0 for i in range(1, 50)]
        
        for x0 in eval_points:
            diff_quot = (f_expr.subs(x, x0 + h) - f_expr.subs(x, x0 - h)) / (2 * h)
            L = sp.limit(diff_quot, h, 0)
            
            if L.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                h1_ok = False
                break
                
            fs_values.append(float(L))
            
        if h1_ok:
            all_greater = all(val > S + 1e-5 for val in fs_values)
            all_less = all(val < S - 1e-5 for val in fs_values)
            neg_q_ok = all_greater or all_less
            return [h1_ok, neg_q_ok]
            
    except Exception:
        pass

    # Fallback to numerical evaluation if symbolic limit fails or times out
    try:
        S = float((f_expr.subs(x, b) - f_expr.subs(x, a)) / (b - a))
        eval_points = [a + (b - a) * i / 50.0 for i in range(1, 50)]
        
        fs_values_num = []
        h_val1 = 1e-6
        h_val2 = 1e-5
        h1_ok_num = True
        
        for x0 in eval_points:
            f_plus1 = float(f_expr.subs(x, x0 + h_val1).evalf())
            f_minus1 = float(f_expr.subs(x, x0 - h_val1).evalf())
            L1 = (f_plus1 - f_minus1) / (2 * h_val1)
            
            f_plus2 = float(f_expr.subs(x, x0 + h_val2).evalf())
            f_minus2 = float(f_expr.subs(x, x0 - h_val2).evalf())
            L2 = (f_plus2 - f_minus2) / (2 * h_val2)
            
            # Check if the numerical symmetric derivative is stable (exists)
            if abs(L1 - L2) > 1e-2 + 1e-2 * abs(L1):
                h1_ok_num = False
                break
            fs_values_num.append(L1)
            
        if not h1_ok_num:
            return [False, False]
            
        all_greater = all(val > S + 1e-4 for val in fs_values_num)
        all_less = all(val < S - 1e-4 for val in fs_values_num)
        
        return [True, all_greater or all_less]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: f_s'(x) exists for all x in (a, b)",
    "¬Q: The secant slope is strictly outside the range of f_s'(x) on (a, b)"
]

N_HYP = 1
NEG_Q_INDEX = 1