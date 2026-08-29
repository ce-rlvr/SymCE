import sympy as sp
from sympy import Symbol, limit, oo, Abs, simplify

# Top-level setup
n = Symbol('n', integer=True)
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: sum_{n=0}^oo a_n x^n is a power series with radius of convergence R",
    "not Q: The truncated power series sum_{n=N}^oo a_n x^n does NOT have radius of convergence equal to R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_radius(a_expr, n_var, start_N):
    if start_N == oo:
        return oo
    if start_N == -oo:
        return None
        
    if hasattr(start_N, 'is_number') and start_N.is_number:
        if not start_N.is_integer:
            return None
        if start_N < 0:
            has_negative_powers = False
            try:
                for i in range(int(start_N), 0):
                    if a_expr.subs(n_var, i) != 0:
                        has_negative_powers = True
                        break
            except Exception:
                pass
            if has_negative_powers:
                return None
    else:
        return None
        
    try:
        if simplify(a_expr) == 0:
            return oo
    except Exception:
        pass
        
    try:
        ratio = Abs(a_expr / a_expr.subs(n_var, n_var + 1))
        L = limit(ratio, n_var, oo)
        if L.is_number and L is not sp.nan:
            return L
    except Exception:
        pass
        
    try:
        root_val = Abs(a_expr)**(1/n_var)
        L = limit(root_val, n_var, oo)
        if L.is_number and L is not sp.nan:
            if L == 0: return oo
            if L == oo: return 0
            return 1/L
    except Exception:
        pass
        
    return None

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a_expr = witness.get('a')
            R_val = witness.get('R')
            N_val = witness.get('N')
        else:
            a_expr, R_val, N_val = witness
            
        if callable(a_expr):
            a_expr = a_expr(n)
            
        if isinstance(a_expr, str):
            a_expr = sp.sympify(a_expr, locals={'n': n, 'x': x})
        else:
            a_expr = sp.sympify(a_expr)
            
        R_val = sp.sympify(R_val)
        N_val = sp.sympify(N_val)
        
        free_symbols = a_expr.free_symbols
        n_sym = next((sym for sym in free_symbols if sym.name == 'n'), n)
        
    except Exception:
        return [False, False]
        
    try:
        R_orig = get_radius(a_expr, n_sym, 0)
        h1_ok = (R_orig is not None) and (R_orig == R_val)
    except Exception:
        h1_ok = False
        
    try:
        R_trunc = get_radius(a_expr, n_sym, N_val)
        neg_q_ok = (R_trunc != R_val)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(neg_q_ok)]