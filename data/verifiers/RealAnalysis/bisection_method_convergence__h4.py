import sympy
from sympy import Symbol, limit, oo, Interval
from sympy.calculus.util import continuous_domain
import math

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: f is a continuous function on the interval",
    "H_2: f(a) * f(b) < 0",
    "H_3: A sequence of intervals is recursively defined starting with the initial interval",
    "¬Q: The sequences do not converge to a common limit c in the interval such that f(c) = 0"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_f_val(f, val):
    if hasattr(f, 'subs'):
        free_syms = list(f.free_symbols)
        if len(free_syms) == 1:
            return float(f.subs(free_syms[0], val))
        elif len(free_syms) == 0:
            return float(f)
        else:
            return float(f.subs(x, val))
    elif callable(f):
        return float(f(val))
    else:
        return float(f)

def get_seq_val(seq, val):
    if isinstance(seq, (list, tuple)):
        if val < len(seq):
            return float(seq[val])
        else:
            return float(seq[-1])
    if hasattr(seq, 'subs'):
        free_syms = list(seq.free_symbols)
        if len(free_syms) == 1:
            return float(seq.subs(free_syms[0], val))
        elif len(free_syms) == 0:
            return float(seq)
        else:
            return float(seq.subs(n, val))
    elif callable(seq):
        return float(seq(val))
    else:
        return float(seq)

def conditions(witness) -> list[bool]:
    try:
        f, a, b, a_seq, b_seq = witness
    except Exception:
        return [False, False, False, False]

    # H1
    try:
        h1 = True
        if hasattr(f, 'subs'):
            try:
                f_expr = sympy.sympify(f)
                free_syms = list(f_expr.free_symbols)
                var = free_syms[0] if len(free_syms) == 1 else x
                domain = continuous_domain(f_expr, var, sympy.S.Reals)
                h1 = (Interval(a, b).is_subset(domain) == True)
            except Exception:
                for i in range(101):
                    try:
                        val = get_f_val(f, a + i * (b - a) / 100.0)
                        if math.isnan(val) or math.isinf(val):
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
        else:
            for i in range(101):
                try:
                    val = get_f_val(f, a + i * (b - a) / 100.0)
                    if math.isnan(val) or math.isinf(val):
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2
    try:
        fa = get_f_val(f, a)
        fb = get_f_val(f, b)
        h2 = (fa * fb < 0)
    except Exception:
        h2 = False

    # H3
    try:
        a0 = get_seq_val(a_seq, 0)
        b0 = get_seq_val(b_seq, 0)
        h3 = (abs(a0 - float(a)) < 1e-7) and (abs(b0 - float(b)) < 1e-7)
        if h3:
            for k in range(11):
                ak = get_seq_val(a_seq, k)
                bk = get_seq_val(b_seq, k)
                if ak > bk + 1e-7:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q
    try:
        neg_q = False
        exact_success = False
        
        if not callable(a_seq) and not callable(b_seq) and not isinstance(a_seq, (list, tuple)) and not isinstance(b_seq, (list, tuple)):
            try:
                a_expr = sympy.sympify(a_seq)
                b_expr = sympy.sympify(b_seq)
                
                var_a = list(a_expr.free_symbols)[0] if len(a_expr.free_symbols) == 1 else n
                var_b = list(b_expr.free_symbols)[0] if len(b_expr.free_symbols) == 1 else n
                
                lim_a = limit(a_expr, var_a, oo)
                lim_b = limit(b_expr, var_b, oo)
                
                if lim_a != lim_b:
                    neg_q = True
                else:
                    c = lim_a
                    if not c.is_real:
                        neg_q = True
                    else:
                        c_val = float(c)
                        if c_val <= float(a) or c_val >= float(b):
                            neg_q = True
                        else:
                            fc = get_f_val(f, c_val)
                            if abs(fc) > 1e-7:
                                neg_q = True
                exact_success = True
            except Exception:
                exact_success = False
                
        if not exact_success:
            try:
                N_val = 10000
                a_N = get_seq_val(a_seq, N_val)
                a_N1 = get_seq_val(a_seq, N_val+1)
                b_N = get_seq_val(b_seq, N_val)
                b_N1 = get_seq_val(b_seq, N_val+1)
            except Exception:
                N_val = 100
                a_N = get_seq_val(a_seq, N_val)
                a_N1 = get_seq_val(a_seq, N_val+1)
                b_N = get_seq_val(b_seq, N_val)
                b_N1 = get_seq_val(b_seq, N_val+1)
                
            if abs(a_N - a_N1) > 1e-3 or abs(b_N - b_N1) > 1e-3:
                neg_q = True
            elif abs(a_N - b_N) > 1e-2:
                neg_q = True
            else:
                c_approx = b_N
                if c_approx <= float(a) + 1e-9 or c_approx >= float(b) - 1e-9:
                    neg_q = True
                else:
                    fc = get_f_val(f, c_approx)
                    if abs(fc) > 1e-2:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]