import sympy
from sympy import symbols, limit, integrate, diff, oo
import math

x, n = symbols('x n')

def check_h1(f_n, a, b):
    try:
        a_f = float(a)
        b_f = float(b)
        if a_f >= b_f:
            return False
        
        xs = [a_f + (b_f - a_f) * i / 200.0 for i in range(201)]
        
        for n_val in [1, 10]:
            for x_val in xs:
                try:
                    val = complex(f_n.subs({n: n_val, x: x_val}).evalf())
                    if abs(val.imag) > 1e-9 or math.isinf(val.real) or math.isnan(val.real):
                        return False
                except Exception:
                    return False
            
        df = diff(f_n, x)
        if df == 0:
            return True
            
        vals = []
        for n_val in [10, 100, 1000]:
            max_df = 0
            for x_val in xs:
                try:
                    v = float(abs(df.subs({n: n_val, x: x_val}).evalf()))
                    if v > max_df:
                        max_df = v
                except Exception:
                    pass
            vals.append(max_df)
            
        if len(vals) == 3:
            if vals[2] > 20 and vals[2] > vals[1] * 1.5:
                return False
                
        return True
    except Exception:
        return False

def check_neg_q(f_n, a, b, f):
    try:
        I_n = integrate(f_n, (x, a, b))
        L = limit(I_n, n, oo)
        I = integrate(f, (x, a, b))
        if L == I:
            return False
        return True
    except Exception:
        pass
        
    try:
        I_val = float(integrate(f, (x, a, b)).evalf())
        In_1000 = float(integrate(f_n.subs(n, 1000), (x, a, b)).evalf())
        In_1001 = float(integrate(f_n.subs(n, 1001), (x, a, b)).evalf())
        In_2000 = float(integrate(f_n.subs(n, 2000), (x, a, b)).evalf())
        
        if abs(In_1000 - I_val) > 1e-2 or abs(In_2000 - I_val) > 1e-2 or abs(In_1000 - In_1001) > 1e-2:
            return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f_n = sympy.sympify(witness['f_n'])
            a = sympy.sympify(witness['a'])
            b = sympy.sympify(witness['b'])
            f = sympy.sympify(witness['f'])
        else:
            f_n, a, b, f = witness
            f_n = sympy.sympify(f_n)
            a = sympy.sympify(a)
            b = sympy.sympify(b)
            f = sympy.sympify(f)
    except Exception:
        return [False, False]
        
    h1_ok = check_h1(f_n, a, b)
    neg_q_ok = check_neg_q(f_n, a, b, f)
    
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f_n is an equicontinuous sequence of real-valued functions on a compact interval",
    "not Q: The sequence of Riemann integrals does not converge to the integral of f"
]

N_HYP = 1
NEG_Q_INDEX = 1