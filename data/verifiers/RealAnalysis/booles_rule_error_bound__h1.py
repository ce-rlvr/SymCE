import sympy
from sympy import Symbol, diff, solveset, S, FiniteSet, integrate, sympify
import math

x = Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_expr = sympify(witness['f'])
            a_val = float(witness['a'])
            b_val = float(witness['b'])
            M_val = float(witness['M'])
        else:
            f_expr = sympify(witness[0])
            a_val = float(witness[1])
            b_val = float(witness[2])
            M_val = float(witness[3])
    except Exception:
        return [False, False]

    free_syms = f_expr.free_symbols
    var = x
    if free_syms and x not in free_syms:
        var = list(free_syms)[0]

    h1_ok = False
    try:
        if M_val > 0:
            a_min = min(a_val, b_val)
            b_max = max(a_val, b_val)
            f6 = diff(f_expr, var, 6)
            pts = [a_min + i * (b_max - a_min) / 100.0 for i in range(101)]
            try:
                f7 = diff(f6, var)
                roots = solveset(f7, var, domain=S.Reals)
                if isinstance(roots, FiniteSet):
                    for r in roots:
                        if r.is_real:
                            r_val = float(r)
                            if a_min <= r_val <= b_max:
                                pts.append(r_val)
            except Exception:
                pass
            
            h1_ok = True
            for pt in pts:
                val = abs(float(f6.subs(var, pt)))
                if val > M_val + 1e-7:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        h = (b_val - a_val) / 4.0
        
        integral_val = float(integrate(f_expr, (var, a_val, b_val)))
        
        boole_sum = 7 * f_expr.subs(var, a_val) + \
                    32 * f_expr.subs(var, a_val + h) + \
                    12 * f_expr.subs(var, a_val + 2*h) + \
                    32 * f_expr.subs(var, a_val + 3*h) + \
                    7 * f_expr.subs(var, b_val)
        boole_val = float(2 * h / 45.0 * boole_sum)
        
        lhs = abs(integral_val - boole_val)
        rhs = 8.0 * M_val * (h**7) / 945.0
        
        if lhs > rhs + 1e-12:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    'H_1: M bounds the sixth derivative on the interval',
    'neg_Q: The error bound fails'
]

N_HYP = 1
NEG_Q_INDEX = 1