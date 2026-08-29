import sympy
from sympy.abc import x
import math

CONDITION_LABELS = [
    "H_1: f is four times continuously differentiable",
    "H_2: fourth derivative bounded by M",
    "H_3: n is an even positive integer",
    "H_4: S_n is the Simpson rule approximation",
    "not_Q: error is strictly greater than the bound"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            n = witness['n']
            M = witness['M']
        else:
            f, a, b, n, M = witness[:5]
            
        if isinstance(f, str):
            f = sympy.sympify(f, locals={'x': x})
    except Exception:
        return [False] * 5

    try:
        f4 = f.diff(x, 4)
        h1 = True
        for i in range(11):
            pt = float(a) + i * (float(b) - float(a)) / 10
            val = f4.subs(x, pt).evalf()
            if not val.is_number or not val.is_finite:
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        h2 = True
        for i in range(101):
            pt = float(a) + i * (float(b) - float(a)) / 100
            val = f4.subs(x, pt).evalf()
            if not val.is_number or not val.is_finite:
                h2 = False
                break
            if float(abs(val)) > float(M) + 1e-9:
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        n_val = float(n)
        h3 = n_val.is_integer() and n_val > 0 and int(n_val) % 2 == 0
    except Exception:
        h3 = False

    try:
        h_step = (float(b) - float(a)) / int(n)
        computed_S_n = float(f.subs(x, a).evalf()) + float(f.subs(x, b).evalf())
        for j in range(1, int(n)):
            pt = float(a) + j * h_step
            val = float(f.subs(x, pt).evalf())
            if j % 2 == 0:
                computed_S_n += 2 * val
            else:
                computed_S_n += 4 * val
        computed_S_n *= h_step / 3
        
        if isinstance(witness, dict) and 'S_n' in witness:
            S_n = float(witness['S_n'])
            h4 = abs(S_n - computed_S_n) < 1e-7
        elif isinstance(witness, (list, tuple)) and len(witness) > 5:
            S_n = float(witness[5])
            h4 = abs(S_n - computed_S_n) < 1e-7
        else:
            S_n = computed_S_n
            h4 = True
    except Exception:
        h4 = False

    try:
        exact_I = float(sympy.Integral(f, (x, a, b)).evalf())
        lhs = abs(exact_I - S_n)
        rhs = float(M) * (float(b) - float(a))**5 / (180 * int(n)**4)
        neg_Q = lhs > rhs + 1e-12
    except Exception:
        neg_Q = False

    return [h1, h2, h3, h4, neg_Q]