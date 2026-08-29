import sympy as sp
from sympy import Symbol, integrate, Interval

x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: m <= f(x) <= M for all x in the interval",
    "¬Q: The bounds m(b - a) <= integral of f(x) dx <= M(b - a) do not hold"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if len(witness) != 5:
            return [False, False]
            
        f_expr, a_val, b_val, m_val, M_val = witness
        
        a = sp.sympify(a_val)
        b = sp.sympify(b_val)
        m = sp.sympify(m_val)
        M = sp.sympify(M_val)
        f = sp.sympify(f_expr)
        
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            x_sym = list(free_syms)[0]
        else:
            x_sym = x
            
        if not (a.is_real and b.is_real):
            return [False, False]
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        if m.is_real and M.is_real:
            try:
                is_empty = bool(a > b)
            except TypeError:
                is_empty = False
                
            if is_empty:
                h1_ok = True
            else:
                domain = Interval(a, b)
                if f.is_constant():
                    val = f.evalf()
                    if m <= val and val <= M:
                        h1_ok = True
                else:
                    less_than_m = sp.solveset(f < m, x_sym, domain=domain)
                    greater_than_M = sp.solveset(f > M, x_sym, domain=domain)
                    
                    if less_than_m.is_empty == True and greater_than_M.is_empty == True:
                        h1_ok = True
                    elif less_than_m.is_empty is None or greater_than_M.is_empty is None:
                        crit_points = sp.solveset(sp.diff(f, x_sym), x_sym, domain=domain)
                        points_to_check = [a, b]
                        if isinstance(crit_points, sp.FiniteSet):
                            points_to_check.extend(list(crit_points))
                        
                        all_within = True
                        for pt in points_to_check:
                            val = f.subs(x_sym, pt).evalf()
                            if not (m <= val and val <= M):
                                all_within = False
                                break
                        if all_within:
                            h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        integral_val = integrate(f, (x_sym, a, b))
        left_bound = m * (b - a)
        right_bound = M * (b - a)
        
        try:
            concl = bool(left_bound <= integral_val) and bool(integral_val <= right_bound)
            neg_q_ok = not concl
        except TypeError:
            concl = bool(left_bound.evalf() <= integral_val.evalf()) and bool(integral_val.evalf() <= right_bound.evalf())
            neg_q_ok = not concl
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]