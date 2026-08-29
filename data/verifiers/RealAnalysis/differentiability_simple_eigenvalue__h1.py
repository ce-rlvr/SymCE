import sympy as sp
from sympy import Symbol, Matrix, limit, oo, nan, simplify, im, S

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (M, a_dict, lambda_0)
    where:
      - M is a sympy Matrix representing the matrix-valued function M(x).
      - a_dict is a dictionary mapping sympy Symbols to their values at point a.
      - lambda_0 is the simple real eigenvalue at M(a).
    """
    try:
        M, a_dict, lambda_0 = witness
    except Exception:
        return [False, False]
    
    # H_1: There is a point a in U such that the matrix M(a) has a simple real eigenvalue lambda_0.
    h1_ok = False
    try:
        M_a = M.subs(a_dict)
        evs = M_a.eigenvals()
        for ev, mult in evs.items():
            diff_val = simplify(ev - lambda_0)
            is_zero = False
            try:
                if diff_val == 0 or abs(float(diff_val)) < 1e-9:
                    is_zero = True
            except Exception:
                if diff_val == 0:
                    is_zero = True
            
            if is_zero:
                im_val = simplify(im(ev))
                is_real = False
                try:
                    if im_val == 0 or abs(float(im_val)) < 1e-9:
                        is_real = True
                except Exception:
                    if im_val == 0:
                        is_real = True
                
                if mult == 1 and is_real:
                    h1_ok = True
                    break
    except Exception:
        h1_ok = False

    # ¬Q: The eigenvalue function lambda(x) is NOT continuously differentiable at a.
    # We find the unique eigenvalue expression that evaluates to lambda_0 at a,
    # and check if it fails to be differentiable at a.
    neg_q_ok = False
    try:
        evs_x = M.eigenvals()
        target_expr = None
        for ev_expr, mult in evs_x.items():
            val_at_a = ev_expr.subs(a_dict)
            diff_val = simplify(val_at_a - lambda_0)
            is_zero = False
            try:
                if diff_val == 0 or abs(float(diff_val)) < 1e-9:
                    is_zero = True
            except Exception:
                if diff_val == 0:
                    is_zero = True
            
            if is_zero:
                target_expr = ev_expr
                break
        
        if target_expr is not None:
            is_diff = True
            h = Symbol('h', real=True)
            for v, val in a_dict.items():
                # Isolate the variable v by substituting the other variables with their values at a
                expr_v = target_expr.subs({k: v_val for k, v_val in a_dict.items() if k != v})
                expr_h = expr_v.subs(v, val + h)
                expr_val = expr_v.subs(v, val)
                
                # Difference quotient
                dq = (expr_h - expr_val) / h
                
                # Left and right limits
                L = limit(dq, h, 0, dir='-')
                R = limit(dq, h, 0, dir='+')
                
                try:
                    if L != R or L.has(oo, -oo, nan) or type(L).__name__ == 'AccumBounds' or type(R).__name__ == 'AccumBounds':
                        is_diff = False
                        break
                except Exception:
                    is_diff = False
                    break
            
            neg_q_ok = not is_diff
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: M(a) has a simple real eigenvalue lambda_0",
    "¬Q: The eigenvalue function lambda(x) is not continuously differentiable at a"
]

N_HYP = 1
NEG_Q_INDEX = 1