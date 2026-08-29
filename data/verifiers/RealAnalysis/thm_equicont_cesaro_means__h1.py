import sympy as sp
import math

# Top-level setup: named object bindings
n = sp.Symbol('n', integer=True, positive=True)
x = sp.Symbol('x', real=True)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, str):
            expr = sp.sympify(witness, locals={'n': n, 'x': x})
        elif callable(witness):
            expr = witness(n, x)
        elif isinstance(witness, tuple) and len(witness) == 2:
            expr = witness[0]
        else:
            expr = witness
    except Exception:
        expr = witness

    def check_equicontinuous(expr):
        try:
            dexpr = sp.diff(expr, x)
            df = sp.lambdify((n, x), dexpr, 'math')
            
            base_max = 0
            for i in range(4001):
                x0 = -2.0 + i * 0.001
                try:
                    v = abs(df(1, x0))
                    if v > base_max:
                        base_max = v
                except Exception:
                    pass
                    
            for n_val in [10, 100, 1000, 10000, 100000]:
                max_val = 0
                for i in range(4001):
                    x0 = -2.0 + i * 0.001
                    try:
                        v = abs(df(n_val, x0))
                        if v > max_val:
                            max_val = v
                    except Exception:
                        pass
                if max_val > 100 and max_val > 10 * base_max:
                    return False
            return True
        except Exception:
            try:
                f = sp.lambdify((n, x), expr, 'math')
                delta = 1e-5
                base_max = 0
                for i in range(4001):
                    x0 = -2.0 + i * 0.001
                    try:
                        v = abs(f(1, x0 + delta) - f(1, x0)) / delta
                        if v > base_max:
                            base_max = v
                    except Exception:
                        pass
                        
                for n_val in [10, 100, 1000, 10000, 100000]:
                    max_val = 0
                    for i in range(4001):
                        x0 = -2.0 + i * 0.001
                        try:
                            v = abs(f(n_val, x0 + delta) - f(n_val, x0)) / delta
                            if v > max_val:
                                max_val = v
                        except Exception:
                            pass
                    if max_val > 100 and max_val > 10 * base_max:
                        return False
                return True
            except Exception:
                return False

    def check_Fn_equicontinuous(expr):
        try:
            dexpr = sp.diff(expr, x)
            df = sp.lambdify((n, x), dexpr, 'math')
            
            base_max = 0
            for i in range(2001):
                x0 = -2.0 + i * 0.002
                try:
                    v = abs(df(1, x0))
                    if v > base_max:
                        base_max = v
                except Exception:
                    pass
                    
            for n_val in [10, 50, 200]:
                max_val = 0
                for i in range(2001):
                    x0 = -2.0 + i * 0.002
                    try:
                        s = sum(df(k, x0) for k in range(1, n_val + 1))
                        v = abs(s / n_val)
                        if v > max_val:
                            max_val = v
                    except Exception:
                        pass
                if max_val > 100 and max_val > 10 * base_max:
                    return False
            return True
        except Exception:
            try:
                f = sp.lambdify((n, x), expr, 'math')
                delta = 1e-5
                base_max = 0
                for i in range(2001):
                    x0 = -2.0 + i * 0.002
                    try:
                        v = abs(f(1, x0 + delta) - f(1, x0)) / delta
                        if v > base_max:
                            base_max = v
                    except Exception:
                        pass
                        
                for n_val in [10, 50, 200]:
                    max_val = 0
                    for i in range(2001):
                        x0 = -2.0 + i * 0.002
                        try:
                            s_plus = sum(f(k, x0 + delta) for k in range(1, n_val + 1))
                            s_minus = sum(f(k, x0) for k in range(1, n_val + 1))
                            v = abs((s_plus - s_minus) / (n_val * delta))
                            if v > max_val:
                                max_val = v
                        except Exception:
                            pass
                    if max_val > 100 and max_val > 10 * base_max:
                        return False
                return True
            except Exception:
                return False

    h1_ok = check_equicontinuous(expr)
    q_ok = check_Fn_equicontinuous(expr)
    neg_q_ok = not q_ok

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: {f_n} is an equicontinuous sequence of real-valued functions on X",
    "¬Q: The sequence of arithmetic means F_n(x) does not form an equicontinuous sequence on X"
]

N_HYP = 1
NEG_Q_INDEX = 1