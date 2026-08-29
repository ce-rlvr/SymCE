import sympy as sp
from sympy import eye, zeros
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    neg_q = False
    
    # Try SymPy approach first if witness is a dict with explicit 'x'
    if isinstance(witness, dict) and 'x' in witness and 'T' in witness:
        try:
            T = witness['T']
            norm_X = witness.get('norm_X')
            norm_Y = witness.get('norm_Y')
            x = witness['x']
            
            if norm_X is not None and norm_Y is not None:
                # Check linearity
                c, x1, x2 = sp.symbols('c x1 x2', real=True)
                T_c = T.subs(x, c*x)
                c_T = c * T
                lin1 = sp.simplify(T_c - c_T) == 0
                
                T_sum = T.subs(x, x1 + x2)
                T_x1 = T.subs(x, x1)
                T_x2 = T.subs(x, x2)
                lin2 = sp.simplify(T_sum - (T_x1 + T_x2)) == 0
                
                h1 = bool(lin1 and lin2)
                
                # Check bounded
                T_expr = T
                norm_Y_T = norm_Y.subs(x, T_expr)
                ratio = sp.simplify(norm_Y_T / norm_X)
                
                is_bounded = True
                try:
                    lim_inf = sp.limit(ratio, x, sp.oo)
                    if lim_inf == sp.oo or lim_inf == -sp.oo or getattr(lim_inf, 'is_infinite', False):
                        is_bounded = False
                    lim_0 = sp.limit(ratio, x, 0)
                    if lim_0 == sp.oo or lim_0 == -sp.oo or getattr(lim_0, 'is_infinite', False):
                        is_bounded = False
                except Exception:
                    pass
                
                max_r = 0
                for val in [1e-9, 1e-7, 1e-5, 1e-3, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0, 100000.0]:
                    try:
                        r = float(ratio.subs(x, val))
                        if r > max_r:
                            max_r = r
                    except Exception:
                        pass
                if max_r > 1000:
                    is_bounded = False
                            
                # Check UC
                try:
                    lim_0_uc = sp.limit(norm_Y_T, x, 0)
                    is_uc = (lim_0_uc == 0)
                except Exception:
                    try:
                        val0 = float(norm_Y_T.subs(x, 1e-9))
                        is_uc = (val0 < 1e-5)
                    except Exception:
                        is_uc = False
                        
                neg_q = (is_uc != is_bounded)
                return [h1, neg_q]
        except Exception:
            pass

    # Fallback to Python function / generic evaluation approach
    try:
        if isinstance(witness, dict):
            T = witness['T']
            norm_X = witness['norm_X']
            norm_Y = witness['norm_Y']
        else:
            T = witness.T
            norm_X = witness.norm_X
            norm_Y = witness.norm_Y
            
        def eval_func(f, val):
            if callable(f):
                return f(val)
            elif hasattr(f, 'subs'):
                syms = list(f.free_symbols)
                if len(syms) == 1:
                    return float(f.subs(syms[0], val))
                elif len(syms) == 0:
                    return float(f)
            raise ValueError("Cannot evaluate")

        # H1: T is linear
        h1 = True
        for a in [1.5, -3.1, 0.0]:
            for b in [2.5, 4.2, 0.0]:
                for c in [1.0, -2.0, 0.0]:
                    try:
                        val1 = eval_func(T, c*a + b)
                        val2 = c * eval_func(T, a) + eval_func(T, b)
                        if abs(val1 - val2) > 1e-7:
                            h1 = False
                    except Exception:
                        h1 = False

        # neg_Q
        max_ratio = 0
        for val in [1e-9, 1e-7, 1e-5, 1e-3, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0, 100000.0]:
            try:
                n_x = float(eval_func(norm_X, val))
                if n_x > 1e-12:
                    t_val = eval_func(T, val)
                    n_y = float(eval_func(norm_Y, t_val))
                    ratio = n_y / n_x
                    if ratio > max_ratio:
                        max_ratio = ratio
            except Exception:
                pass
        is_bounded = max_ratio < 1000
        
        try:
            t_val0 = eval_func(T, 1e-9)
            lim_0 = float(eval_func(norm_Y, t_val0))
            is_uc = lim_0 < 1e-5
        except Exception:
            is_uc = False
            
        neg_q = (is_uc != is_bounded)
        
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T: X -> Y is a linear operator",
    "¬Q: Uniform continuity is not equivalent to boundedness"
]
N_HYP = 1
NEG_Q_INDEX = 1