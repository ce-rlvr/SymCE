import sympy as sp
import math

x, y = sp.symbols('x y', real=True)

CONDITION_LABELS = [
    "H_1: f is continuous and strictly increasing on the interval 0 to c",
    "H_2: f(0) = 0",
    "not Q: The inequality or its equality condition fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def safe_float(expr):
    try:
        val = sp.N(expr)
        return float(val)
    except Exception:
        return float('nan')

def conditions(witness):
    """
    witness is expected to be a tuple: (f_expr, f_inv_expr, c_val, a_val, b_val)
    where f_expr is a sympy expression in terms of x,
    f_inv_expr is a sympy expression in terms of y (the inverse of f),
    and c_val, a_val, b_val are real numbers.
    """
    try:
        f_expr, f_inv_expr, c_val, a_val, b_val = witness
    except Exception:
        return [False, False, False]
        
    # H_1: f is continuous and strictly increasing on 0 to c
    h1_ok = False
    try:
        c_float = safe_float(c_val)
        if not math.isnan(c_float) and c_float > 0:
            pts = [c_float * i / 100.0 for i in range(101)]
            vals = [safe_float(f_expr.subs(x, p)) for p in pts]
            if not any(math.isnan(v) or math.isinf(v) for v in vals):
                h1_ok = all(vals[i] < vals[i+1] for i in range(100))
    except Exception:
        h1_ok = False

    # H_2: f(0) = 0
    h2_ok = False
    try:
        f0 = safe_float(f_expr.subs(x, 0))
        h2_ok = not math.isnan(f0) and abs(f0) < 1e-7
    except Exception:
        h2_ok = False

    # not Q: The conclusion fails
    neg_q_ok = False
    try:
        b_float = safe_float(b_val)
        a_float = safe_float(a_val)
        
        if math.isnan(b_float) or math.isnan(a_float):
            return [h1_ok, h2_ok, False]
            
        # Verify that f_inv_expr is indeed the inverse of f on the interval 0 to b
        inv_valid = True
        if b_float > 0:
            y_pts = [b_float * i / 10.0 for i in range(11)]
        elif b_float < 0:
            y_pts = [b_float * i / 10.0 for i in range(11)]
        else:
            y_pts = [0.0]
            
        for yp in y_pts:
            x_val = safe_float(f_inv_expr.subs(y, yp))
            if math.isnan(x_val):
                inv_valid = False
                break
            y_val = safe_float(f_expr.subs(x, x_val))
            if math.isnan(y_val) or abs(y_val - yp) > 1e-5:
                inv_valid = False
                break
                
        if inv_valid:
            # Compute the integrals numerically
            int_a = safe_float(sp.Integral(f_expr, (x, 0, a_float)).evalf())
            int_b = safe_float(sp.Integral(f_inv_expr, (y, 0, b_float)).evalf())
            
            if not (math.isnan(int_a) or math.isnan(int_b)):
                LHS = int_a + int_b
                RHS = a_float * b_float
                
                fa_val = safe_float(f_expr.subs(x, a_float))
                if not math.isnan(fa_val):
                    ineq_holds = LHS >= RHS - 1e-5
                    eq_holds = abs(LHS - RHS) < 1e-5
                    iff_holds = abs(b_float - fa_val) < 1e-5
                    
                    # The conclusion states: LHS >= RHS, with equality if and only if b = f(a)
                    conclusion_holds = ineq_holds and (eq_holds == iff_holds)
                    neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]