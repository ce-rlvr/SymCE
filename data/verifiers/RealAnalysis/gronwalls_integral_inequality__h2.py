import sympy
import math

t = sympy.Symbol('t', real=True)
s = sympy.Symbol('s', real=True)

def conditions(witness):
    try:
        a = float(witness['a'])
        b = float(witness['b'])
        alpha = float(witness['alpha'])
        u_expr = sympy.sympify(witness['u']).subs(s, t)
        beta_expr = sympy.sympify(witness['beta']).subs(s, t)
        
        u_f = sympy.lambdify(t, u_expr, modules=['math'])
        beta_f = sympy.lambdify(t, beta_expr, modules=['math'])
    except Exception:
        return [False] * 5

    try:
        h1 = a < b
    except Exception:
        h1 = False

    try:
        h2 = True
        for i in range(101):
            ti = a + i * (b - a) / 100.0
            val = u_f(ti)
            if not math.isfinite(float(val)):
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        h3 = alpha >= 0.0
    except Exception:
        h3 = False

    try:
        h4 = True
        n_steps = 2000
        dt = (b - a) / n_steps
        
        integral_val = 0.0
        u_val = float(u_f(a))
        beta_val = float(beta_f(a))
        integrand_prev = beta_val * u_val
        
        if u_val > alpha + integral_val + 1e-5:
            h4 = False
            
        if h4:
            for i in range(1, n_steps + 1):
                ti = a + i * dt
                u_val = float(u_f(ti))
                beta_val = float(beta_f(ti))
                integrand_curr = beta_val * u_val
                
                integral_val += 0.5 * (integrand_prev + integrand_curr) * dt
                integrand_prev = integrand_curr
                
                if u_val > alpha + integral_val + 1e-5:
                    h4 = False
                    break
    except Exception:
        h4 = False

    try:
        neg_q = False
        n_steps = 2000
        dt = (b - a) / n_steps
        
        integral_beta = 0.0
        beta_prev = float(beta_f(a))
        
        u_val = float(u_f(a))
        if u_val > alpha * math.exp(integral_beta) + 1e-5:
            neg_q = True
            
        if not neg_q:
            for i in range(1, n_steps + 1):
                ti = a + i * dt
                u_val = float(u_f(ti))
                beta_curr = float(beta_f(ti))
                
                integral_beta += 0.5 * (beta_prev + beta_curr) * dt
                beta_prev = beta_curr
                
                if u_val > alpha * math.exp(integral_beta) + 1e-5:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: I is a closed interval from a to b",
    "H_2: u is a continuous function on I",
    "H_3: alpha is a non-negative real constant",
    "H_4: For all t in I, u(t) <= alpha + int_a^t beta(s) u(s) ds",
    "¬Q: There exists t in I such that u(t) > alpha * exp(int_a^t beta(s) ds)"
]

N_HYP = 4
NEG_Q_INDEX = 4