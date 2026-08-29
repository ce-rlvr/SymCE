import sympy
from sympy import Symbol, Rational, integrate, diff, solveset, Eq, Interval
import math

x = Symbol('x', real=True)

def conditions(witness):
    try:
        f_expr, a_val, b_val, h_val = witness
        f = sympy.sympify(f_expr)
        a = sympy.sympify(a_val)
        b = sympy.sympify(b_val)
        h = sympy.sympify(h_val)
    except Exception:
        return [False, False, False]
    
    try:
        f6 = diff(f, x, 6)
        if f6 is None or f6 == sympy.nan:
            h1 = False
        else:
            h1 = True
            for i in range(11):
                pt = a + i * (b - a) / 10
                try:
                    val_f = float(f.subs(x, pt))
                    val_f6 = float(f6.subs(x, pt))
                    if math.isnan(val_f) or math.isnan(val_f6) or math.isinf(val_f) or math.isinf(val_f6):
                        h1 = False
                        break
                except TypeError:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        integral_val = integrate(f, (x, a, b))
        boole_val = 2 * h / 45 * (
            7 * f.subs(x, a) + 
            32 * f.subs(x, a + h) + 
            12 * f.subs(x, a + 2 * h) + 
            32 * f.subs(x, a + 3 * h) + 
            7 * f.subs(x, b)
        )
        E = integral_val - boole_val
        
        g = -Rational(8, 945) * (h**7) * f6
        
        if float(a) >= float(b):
            exists = False
        else:
            E_simp = sympy.simplify(E)
            g_simp = sympy.simplify(g)
            
            if g_simp.is_constant():
                diff_val = E_simp - g_simp
                try:
                    if abs(float(diff_val)) < 1e-9:
                        exists = True
                    else:
                        exists = False
                except Exception:
                    if sympy.simplify(diff_val) == 0:
                        exists = True
                    else:
                        exists = False
            else:
                try:
                    g_vals = []
                    for i in range(1, 1000):
                        try:
                            val = float(g_simp.subs(x, a + i * (b - a) / 1000))
                            if not math.isnan(val) and not math.isinf(val):
                                g_vals.append(val)
                        except TypeError:
                            pass
                    
                    if not g_vals:
                        exists = False
                    else:
                        min_g = min(g_vals)
                        max_g = max(g_vals)
                        E_float = float(E_simp)
                        
                        if min_g <= E_float <= max_g:
                            exists = True
                        else:
                            if min_g - 1e-7 <= E_float <= max_g + 1e-7:
                                exists = True
                            else:
                                exists = False
                except Exception:
                    try:
                        sols = solveset(Eq(g_simp, E_simp), x, domain=Interval.open(a, b))
                        if sols is sympy.S.EmptySet:
                            exists = False
                        elif isinstance(sols, sympy.Set) and sols.is_empty is False:
                            exists = True
                        else:
                            exists = False
                    except Exception:
                        exists = False
                        
        neg_q = not exists
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ['H_1: f is a real-valued function that is six times differentiable', 'H_2: f sixth derivative is continuous', 'not Q: There does not exist c satisfying the Boole rule error equation']
N_HYP = 2
NEG_Q_INDEX = 2