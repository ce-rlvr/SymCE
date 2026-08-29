import sympy
from sympy import catalan, Symbol, Rational, limit, oo, Abs, zoo, solve
from sympy.abc import x, n
import math

# Top-level setup
# (No specific named groups needed for Real Analysis, but we define x and n for convenience)

def compute_R(a_n):
    try:
        free = a_n.free_symbols
        n_vars = [v for v in free if v.name == 'n']
        if n_vars:
            n_var = n_vars[0]
        else:
            return None
            
        x_vars = [v for v in free if v.name != 'n']
        
        a_n_plus_1 = a_n.subs(n_var, n_var + 1)
        
        ratio = Abs(a_n_plus_1 / a_n)
        L = limit(ratio, n_var, oo)
        
        if L == 0:
            return float('inf')
        if L == oo or L == zoo:
            return 0.0
            
        if not x_vars:
            c = float(L)
            return 1.0 / c if c != 0 else float('inf')
            
        x_var = x_vars[0]
        
        ratio_no_abs = a_n_plus_1 / a_n
        L_no_abs = limit(ratio_no_abs, n_var, oo)
        
        try:
            roots = solve(L_no_abs, x_var)
            if roots:
                x0 = complex(roots[0]).real
            else:
                x0 = 0.0
        except Exception:
            x0 = 0.0
            
        c = float(L.subs(x_var, x0 + 1))
        L2 = float(L.subs(x_var, x0 + 2))
        k = math.log2(L2 / c)
        if k == 0:
            return 1.0 / c if c != 0 else float('inf')
        R = (1/c)**(1/k)
        return R
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    C_n_obj = None
    R_obj = None
    
    if isinstance(witness, dict):
        C_n_obj = witness.get('C_n', witness.get('C'))
        R_obj = witness.get('R', witness.get('radius', witness.get('a_n', witness.get('power_series'))))
    elif isinstance(witness, tuple) or isinstance(witness, list):
        if len(witness) >= 1:
            C_n_obj = witness[0]
        if len(witness) >= 2:
            R_obj = witness[1]
    else:
        C_n_obj = getattr(witness, 'C_n', getattr(witness, 'C', witness))
        R_obj = getattr(witness, 'R', getattr(witness, 'radius', getattr(witness, 'a_n', witness)))
        
    h1_ok = False
    try:
        catalans = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862]
        is_cat = True
        for i, val in enumerate(catalans):
            c_val = None
            if callable(C_n_obj):
                try:
                    c_val = C_n_obj(i)
                except Exception:
                    pass
            if c_val is None and isinstance(C_n_obj, (list, tuple)):
                try:
                    c_val = C_n_obj[i]
                except Exception:
                    pass
            if c_val is None and hasattr(C_n_obj, 'subs'):
                try:
                    free_vars = list(C_n_obj.free_symbols)
                    if len(free_vars) == 1:
                        c_val = C_n_obj.subs(free_vars[0], i)
                    else:
                        from sympy.abc import n as sym_n
                        c_val = C_n_obj.subs(sym_n, i)
                except Exception:
                    pass
            
            if c_val is None:
                is_cat = False
                break
                
            if int(float(c_val)) != val:
                is_cat = False
                break
        h1_ok = is_cat
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        R_val = None
        if R_obj is not None:
            try:
                R_val = float(R_obj)
            except Exception:
                R_val = compute_R(R_obj)
                
        if R_val is not None:
            if abs(R_val - 0.25) > 1e-7:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The sequence {C_n} is the sequence of Catalan numbers",
    "¬Q: The radius of convergence of the power series is not 1/4"
]

N_HYP = 1
NEG_Q_INDEX = 1