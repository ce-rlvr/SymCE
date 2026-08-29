import sympy
from sympy import S, Interval, oo, limit, Piecewise, Abs, lambdify
from sympy.calculus.util import continuous_domain
import math

# Top-level setup for witness expressions
x, n = sympy.symbols('x n')

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of functions defined on D",
    "H_2: Each function f_n is continuous on D",
    "H_3: The sequence (f_n) converges uniformly to a function f on D",
    "¬Q: The limit function f is not continuous on D"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        f_n = witness['f_n']
        f = witness['f']
        D = witness['D']
        x_sym = witness['x']
        n_sym = witness['n']
    except KeyError:
        return [False, False, False, False]

    # H1: (f_n) is a sequence of functions defined on D
    h1 = False
    try:
        h1_ok = True
        test_points = []
        if D.is_Interval and D.start != -oo and D.end != oo:
            test_points = [D.start, D.end, (D.start + D.end)/2]
        else:
            test_points = [0, 1, -1]
        for i in [1, 2, 3]:
            for p in test_points:
                val = f_n.subs({n_sym: i, x_sym: p})
                if val.has(S.NaN) or val.has(S.ComplexInfinity) or val.has(S.Infinity) or val.has(S.NegativeInfinity):
                    h1_ok = False
                    break
            if not h1_ok:
                break
        h1 = h1_ok
    except Exception:
        h1 = False

    # H2: Each function f_n is continuous on D
    h2 = False
    try:
        h2_ok = True
        for i in [1, 2, 3]:
            f_i = f_n.subs(n_sym, i)
            dom = continuous_domain(f_i, x_sym, S.Reals)
            if not D.is_subset(dom):
                h2_ok = False
                break
        h2 = h2_ok
    except Exception:
        h2 = False

    # H3: The sequence (f_n) converges uniformly to a function f on D
    h3 = False
    try:
        points = []
        if D.is_Interval:
            start = float(D.start) if D.start != -oo else -100.0
            end = float(D.end) if D.end != oo else 100.0
            width = end - start
            points = [start + width * i / 1000.0 for i in range(1001)]
        elif D == S.Reals:
            points = [float(i)/10.0 for i in range(-1000, 1001)]
        elif hasattr(D, 'args'):
            try:
                points = [float(arg) for arg in D.args if arg.is_real]
            except Exception:
                points = [0.0]
        else:
            points = [0.0]
            
        max_diffs = []
        for n_val in [10, 100, 1000, 10000]:
            f_n_val = f_n.subs(n_sym, n_val)
            try:
                func = lambdify(x_sym, Abs(f_n_val - f), modules=['math', 'sympy'])
                m = 0.0
                for p in points:
                    try:
                        val = float(func(p))
                        if val > m:
                            m = val
                    except Exception:
                        pass
                max_diffs.append(m)
            except Exception:
                m = 0.0
                for p in points:
                    try:
                        val = float(Abs(f_n_val - f).subs(x_sym, p))
                        if val > m:
                            m = val
                    except Exception:
                        pass
                max_diffs.append(m)
                
        if len(max_diffs) == 4:
            if max_diffs[-1] <= 1e-4:
                h3 = True
            elif max_diffs[-1] < 1e-2 and max_diffs[-1] < max_diffs[0] * 0.1:
                h3 = True
            else:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: The limit function f is not continuous on D
    neg_q = False
    try:
        dom = continuous_domain(f, x_sym, S.Reals)
        if not D.is_subset(dom):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]