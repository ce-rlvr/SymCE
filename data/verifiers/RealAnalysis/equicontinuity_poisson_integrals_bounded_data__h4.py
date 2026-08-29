import math
import sympy as sp

# Top-level setup: symbols that the witness expressions may reference
n, r, theta = sp.symbols('n r theta')

def get_val(witness, key):
    if isinstance(witness, dict):
        return witness[key]
    return getattr(witness, key)

def evaluate_B(B_obj, n_val, theta_val):
    if callable(B_obj):
        val = B_obj(n_val, theta_val)
    elif hasattr(B_obj, 'subs'):
        val = B_obj.subs({n: n_val, theta: theta_val}).evalf()
    else:
        val = B_obj
    return complex(val)

def evaluate_F(F_obj, n_val, r_val, theta_val):
    if callable(F_obj):
        val = F_obj(n_val, r_val, theta_val)
    elif hasattr(F_obj, 'subs'):
        val = F_obj.subs({n: n_val, r: r_val, theta: theta_val}).evalf()
    else:
        val = F_obj
    return complex(val)

def evaluate_p(p_obj, n_val):
    if callable(p_obj):
        return p_obj(n_val)
    else:
        r_expr, th_expr = p_obj
        r_val = float(r_expr.subs({n: n_val}).evalf()) if hasattr(r_expr, 'subs') else float(r_expr)
        th_val = float(th_expr.subs({n: n_val}).evalf()) if hasattr(th_expr, 'subs') else float(th_expr)
        return (r_val, th_val)

def conditions(witness) -> list[bool]:
    # H_1: Let D be the open unit disk in R^2 and dD be its boundary circle.
    # This is contextual setup.
    h1 = True
    
    # H_2: Let B be a family of measurable functions on dD.
    try:
        B_obj = get_val(witness, 'B')
        _ = evaluate_B(B_obj, 1, 0.0)
        h2 = True
    except Exception:
        h2 = False
        
    # H_3: Assume there exists a constant M > 0 such that |g(zeta)| <= M for almost every zeta in dD and all g in B.
    try:
        M = float(get_val(witness, 'M'))
        B_obj = get_val(witness, 'B')
        h3 = M > 0
        if h3:
            # Check boundedness over a grid of parameters
            for n_val in range(1, 20):
                for i in range(100):
                    theta_val = 2 * math.pi * i / 100
                    if abs(evaluate_B(B_obj, n_val, theta_val)) > M + 1e-7:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False
        
    # H_4: Let K be a compact subset of the open disk D.
    try:
        K_r = float(get_val(witness, 'K_r'))
        h4 = 0 <= K_r < 1.0
    except Exception:
        h4 = False
        
    # neg_Q: The family F is NOT uniformly equicontinuous on K.
    try:
        p1_obj = get_val(witness, 'p1')
        p2_obj = get_val(witness, 'p2')
        F_obj = get_val(witness, 'F')
        K_r = float(get_val(witness, 'K_r'))
        
        neg_q = False
        # Look for a sequence index n where equicontinuity fails
        for n_val in [10, 100, 1000, 10000]:
            r1, th1 = evaluate_p(p1_obj, n_val)
            r2, th2 = evaluate_p(p2_obj, n_val)
            
            in_K = (0 <= r1 <= K_r) and (0 <= r2 <= K_r)
            
            x1, y1 = r1 * math.cos(th1), r1 * math.sin(th1)
            x2, y2 = r2 * math.cos(th2), r2 * math.sin(th2)
            dist = math.hypot(x1 - x2, y1 - y2)
            
            f1 = evaluate_F(F_obj, n_val, r1, th1)
            f2 = evaluate_F(F_obj, n_val, r2, th2)
            diff = abs(f1 - f2)
            
            # If distance shrinks but function difference remains large, equicontinuity fails
            if in_K and (dist < 2.0 / n_val) and (diff > 0.1):
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: D is the open unit disk and dD is its boundary",
    "H_2: B is a family of measurable functions on dD",
    "H_3: There exists M > 0 such that |g| <= M for all g in B",
    "H_4: K is a compact subset of the open disk D",
    "¬Q: The family F is not uniformly equicontinuous on K"
]

N_HYP = 4
NEG_Q_INDEX = 4