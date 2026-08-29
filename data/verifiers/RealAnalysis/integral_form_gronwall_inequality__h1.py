import sympy
import math
from sympy import Symbol

t = Symbol('t', real=True)
s = Symbol('s', real=True)

def conditions(witness):
    try:
        local_dict = {'t': t, 's': s, 'exp': sympy.exp, 'sin': sympy.sin, 'cos': sympy.cos, 'pi': sympy.pi}
        if isinstance(witness, dict):
            a = sympy.sympify(witness['a'], locals=local_dict)
            b = sympy.sympify(witness['b'], locals=local_dict)
            beta = sympy.sympify(witness['beta'], locals=local_dict)
            alpha = sympy.sympify(witness['alpha'], locals=local_dict)
            u = sympy.sympify(witness['u'], locals=local_dict)
        else:
            a, b, beta, alpha, u = [sympy.sympify(x, locals=local_dict) for x in witness]
            
        generic_t = sympy.Symbol('t')
        a = a.subs(generic_t, t)
        b = b.subs(generic_t, t)
        beta = beta.subs(generic_t, t)
        alpha = alpha.subs(generic_t, t)
        u = u.subs(generic_t, t)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(float(beta) >= 0)
    except Exception:
        h1 = False

    try:
        a_val = float(a)
        b_val = float(b)
        if a_val >= b_val:
            h2 = False
        else:
            h2 = True
            N = 1000
            step = (b_val - a_val) / N
            integral_val = 0.0
            
            try:
                u_val = float(u.subs(t, a_val).evalf())
                if float(beta) + integral_val - u_val < -1e-4:
                    h2 = False
            except Exception:
                pass
                
            prev_integrand = None
            try:
                prev_integrand = float((alpha * u).subs(t, a_val).evalf())
            except Exception:
                pass

            if h2:
                for i in range(1, N + 1):
                    t_val = a_val + i * step
                    try:
                        curr_integrand = float((alpha * u).subs(t, t_val).evalf())
                        if prev_integrand is not None:
                            integral_val += 0.5 * step * (prev_integrand + curr_integrand)
                        else:
                            integral_val += step * curr_integrand
                        prev_integrand = curr_integrand
                        
                        u_val = float(u.subs(t, t_val).evalf())
                        if float(beta) + integral_val - u_val < -1e-4:
                            h2 = False
                            break
                    except Exception:
                        prev_integrand = None
    except Exception:
        h2 = False

    try:
        a_val = float(a)
        b_val = float(b)
        if a_val >= b_val:
            neg_q = False
        else:
            neg_q = False
            N = 1000
            step = (b_val - a_val) / N
            integral_alpha_val = 0.0
            
            try:
                u_val = float(u.subs(t, a_val).evalf())
                if float(beta) == 0.0:
                    rhs_q_val = 0.0
                else:
                    rhs_q_val = float(beta) * math.exp(integral_alpha_val)
                if rhs_q_val - u_val < -1e-4:
                    neg_q = True
            except Exception:
                pass
                
            prev_alpha = None
            try:
                prev_alpha = float(alpha.subs(t, a_val).evalf())
            except Exception:
                pass

            if not neg_q:
                for i in range(1, N + 1):
                    t_val = a_val + i * step
                    try:
                        curr_alpha = float(alpha.subs(t, t_val).evalf())
                        if prev_alpha is not None:
                            integral_alpha_val += 0.5 * step * (prev_alpha + curr_alpha)
                        else:
                            integral_alpha_val += step * curr_alpha
                        prev_alpha = curr_alpha
                        
                        u_val = float(u.subs(t, t_val).evalf())
                        
                        try:
                            if float(beta) == 0.0:
                                rhs_q_val = 0.0
                            else:
                                rhs_q_val = float(beta) * math.exp(integral_alpha_val)
                        except OverflowError:
                            rhs_q_val = float('inf')
                            
                        if rhs_q_val - u_val < -1e-4:
                            neg_q = True
                            break
                    except Exception:
                        prev_alpha = None
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    'H_1: beta is a non-negative real constant',
    'H_2: u(t) <= beta + integral of alpha(s)u(s) ds for all t in (a,b)',
    'not Q: u(t) <= beta * exp(integral of alpha(s) ds) fails for some t in (a,b)'
]

N_HYP = 2
NEG_Q_INDEX = 2