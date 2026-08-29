import sympy
import math

# Top-level setup
n = sympy.Symbol('n', integer=True, nonnegative=True)

def check_convergence(expr):
    try:
        s = sympy.Sum(expr, (n, 0, sympy.oo))
        c = s.is_convergent()
        if c is True: return True
        if c is False: return False
        
        val = s.doit()
        if val.is_finite is True: return True
        if val.is_finite is False: return False
        
        # Heuristic for alternating series if symbolic evaluation fails
        f = sympy.lambdify(n, expr, 'math')
        try:
            v1 = float(f(1000))
            v2 = float(f(1001))
            v3 = float(f(1002))
        except Exception:
            v1 = float(expr.subs(n, 1000).evalf())
            v2 = float(expr.subs(n, 1001).evalf())
            v3 = float(expr.subs(n, 1002).evalf())
            
        if abs(v1) < 0.5 and (v1 * v2 < 0) and (v2 * v3 < 0):
            return True
            
        return False
    except Exception:
        return False

def check_neg_q_numerically(a_expr, b_expr):
    try:
        a_func = sympy.lambdify(n, a_expr, 'math')
        b_func = sympy.lambdify(n, b_expr, 'math')
        
        a_vals = []
        b_vals = []
        for i in range(401):
            try:
                v_a = float(a_func(i))
            except Exception:
                try:
                    v_a = float(a_expr.subs(n, i).evalf())
                except Exception:
                    v_a = 0.0
            a_vals.append(v_a)
            
            try:
                v_b = float(b_func(i))
            except Exception:
                try:
                    v_b = float(b_expr.subs(n, i).evalf())
                except Exception:
                    v_b = 0.0
            b_vals.append(v_b)
            
        c_vals = []
        for m_val in range(401):
            c_m = sum(a_vals[k_val] * b_vals[m_val - k_val] for k_val in range(m_val + 1))
            c_vals.append(c_m)
            
        max_c = max(abs(v) for v in c_vals)
        if max_c == 0:
            return False
            
        # If the tail of the Cauchy product sequence is still a significant fraction 
        # of its peak, it is not converging to 0, hence the series diverges.
        tail_max = max(abs(c_vals[i]) for i in range(390, 401))
        if tail_max > 0.2 * max_c:
            return True
            
        # If c_m -> 0, check if the sum converges to A * B
        C_N = sum(c_vals)
        A_N = sum(a_vals)
        B_N = sum(b_vals)
        
        expected = A_N * B_N
        if abs(expected) > 1e-9:
            if abs(C_N - expected) / abs(expected) > 0.2:
                return True
        else:
            if abs(C_N - expected) > 0.2 * max_c:
                return True
                
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            a_expr = witness[0](n) if callable(witness[0]) else witness[0]
            b_expr = witness[1](n) if callable(witness[1]) else witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    h1 = check_convergence(a_expr) and check_convergence(b_expr)
    neg_q = check_neg_q_numerically(a_expr, b_expr)
    
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sum a_n and sum b_n are convergent infinite series",
    "¬Q: The Cauchy product series does not converge to AB"
]

N_HYP = 1
NEG_Q_INDEX = 1