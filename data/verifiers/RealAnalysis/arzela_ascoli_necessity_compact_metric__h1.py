import sympy as sp
from sympy import symbols, Interval, oo, limit, maximum, simplify, Abs
from sympy.calculus.util import continuous_domain

# Top-level setup
x = symbols('x', real=True)
n, m = symbols('n m', real=True, positive=True)

CONDITION_LABELS = [
    "H_1: {f_n} is a sequence of continuous real-valued functions on K",
    "H_2: {f_n} converges uniformly to f on K",
    "¬Q: {f_n} is NOT uniformly equicontinuous on K"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    witness is a dictionary with:
      'K': sympy Set (e.g., sp.S.Reals, Interval(0, oo))
      'f_n': sympy expression in x and n
      'f': sympy expression in x
      'x_m': sympy expression in m (sequence in K)
      'y_m': sympy expression in m (sequence in K)
      'n_m': sympy expression in m (or constant, default 1)
    """
    K = witness.get('K')
    f_n = witness.get('f_n')
    f = witness.get('f')
    x_m = witness.get('x_m')
    y_m = witness.get('y_m')
    n_m = witness.get('n_m', 1)
    
    # H_1: {f_n} is a sequence of continuous real-valued functions on K
    try:
        h1_ok = True
        for n_val in [1, 2, 3]:
            fn_val = f_n.subs(n, n_val)
            dom = continuous_domain(fn_val, x, sp.S.Reals)
            if not dom.is_superset(K):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H_2: {f_n} converges uniformly to f on K
    try:
        diff = simplify(f_n - f)
        if diff == 0:
            h2_ok = True
        elif not diff.has(x):
            lim_max = limit(Abs(diff), n, oo)
            h2_ok = (lim_max == 0)
        else:
            max_diff = maximum(Abs(diff), x, K)
            lim_max = limit(max_diff, n, oo)
            h2_ok = (lim_max == 0)
    except Exception:
        h2_ok = False

    # ¬Q: {f_n} is NOT uniformly equicontinuous on K
    try:
        # Check if x_m, y_m are in K for large m
        m_val = 1000000
        x_m_val = x_m.subs(m, m_val)
        y_m_val = y_m.subs(m, m_val)
        
        try:
            in_K = (K.contains(x_m_val) == True) and (K.contains(y_m_val) == True)
        except Exception:
            in_K = False
            
        if not in_K:
            neg_q_ok = False
        else:
            # 1. |x_m - y_m| -> 0 as m -> oo
            diff_xy = limit(Abs(x_m - y_m), m, oo)
            cond1 = (diff_xy == 0)
            
            # 2. |f_{n_m}(x_m) - f_{n_m}(y_m)| does not go to 0
            fn_m = f_n.subs(n, n_m)
            val_x = fn_m.subs(x, x_m)
            val_y = fn_m.subs(x, y_m)
            diff_f = limit(Abs(val_x - val_y), m, oo)
            cond2 = (diff_f != 0)
            
            neg_q_ok = cond1 and cond2
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]