import sympy as sp
from sympy.abc import x
import math

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 5:
            return witness
        elif len(witness) == 3:
            f, L, alpha = witness
            return f, 0.0, 1.0, L, alpha
    elif isinstance(witness, dict):
        f = witness['f']
        a = witness.get('a', 0.0)
        b = witness.get('b', 1.0)
        L = witness['L']
        alpha = witness['alpha']
        return f, a, b, L, alpha
    raise ValueError("Invalid witness format")

def eval_f(f, val):
    if hasattr(f, 'free_symbols'):
        syms = list(f.free_symbols)
        if len(syms) == 1:
            return float(f.subs(syms[0], val))
        elif len(syms) == 0:
            return float(f)
        else:
            raise ValueError("Too many free symbols in sympy expression")
    else:
        return float(f(val))

def conditions(witness) -> list[bool]:
    def check_h1():
        try:
            f, a, b, L, alpha = parse_witness(witness)
            a_val = float(a)
            b_val = float(b)
            if not (a_val < b_val):
                return False
            
            for pt in [a_val, b_val, (a_val + b_val) / 2]:
                v = eval_f(f, pt)
                if not isinstance(v, float) or math.isnan(v) or math.isinf(v):
                    return False
            return True
        except Exception:
            return False

    def check_h2():
        try:
            f, a, b, L, alpha = parse_witness(witness)
            a_val = float(a)
            b_val = float(b)
            L_val = float(L)
            alpha_val = float(alpha)
            
            if L_val < 0:
                return False
            
            N = 50
            points = [a_val + (b_val - a_val) * i / (N - 1) for i in range(N)]
            f_vals = [eval_f(f, pt) for pt in points]
            
            for i in range(N):
                for j in range(i + 1, N):
                    x_val = points[i]
                    y_val = points[j]
                    diff = abs(f_vals[i] - f_vals[j])
                    bound = L_val * (abs(x_val - y_val) ** alpha_val)
                    
                    if diff > bound + 1e-7:
                        return False
            return True
        except Exception:
            return False

    def check_neg_q():
        try:
            f, a, b, L, alpha = parse_witness(witness)
            a_val = float(a)
            b_val = float(b)
            
            N = 20
            points = [a_val + (b_val - a_val) * i / (N - 1) for i in range(N)]
            f_vals = [eval_f(f, pt) for pt in points]
            
            fa = f_vals[0]
            for val in f_vals:
                if abs(val - fa) > 1e-7:
                    return True
            return False
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]

CONDITION_LABELS = ['H_1: f is a real-valued function defined on an interval', 'H_2: f satisfies Holder condition', 'neg_Q: f is not a constant function']
N_HYP = 2
NEG_Q_INDEX = 2