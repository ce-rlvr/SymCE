import sympy
import math

x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            K = witness['K']
        else:
            f, a, b, K = witness
        f = sympy.sympify(f)
    except Exception:
        return [False, False]

    try:
        a = float(a)
        b = float(b)
        K = float(K)
        h1 = (a < b)
        if h1:
            f_lam = sympy.lambdify(x, f, 'math')
            df = sympy.diff(f, x)
            df_lam = sympy.lambdify(x, df, 'math')
            for i in range(101):
                try:
                    val = float(f_lam(a + i * (b - a) / 100.0))
                except TypeError:
                    val = float(f_lam())
                if val <= 0 or not math.isfinite(val):
                    h1 = False
                    break
                try:
                    dval = float(df_lam(a + i * (b - a) / 100.0))
                except TypeError:
                    dval = float(df_lam())
                if not math.isfinite(dval):
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        f_lam = sympy.lambdify(x, f, 'math')
        n = 1000
        h_step = (b - a) / n
        
        try:
            s = float(f_lam(a)) + float(f_lam(b))
        except TypeError:
            s = float(f_lam()) + float(f_lam())
            
        for i in range(1, n, 2):
            try:
                s += 4 * float(f_lam(a + i * h_step))
            except TypeError:
                s += 4 * float(f_lam())
        for i in range(2, n-1, 2):
            try:
                s += 2 * float(f_lam(a + i * h_step))
            except TypeError:
                s += 2 * float(f_lam())
                
        integral_val = s * h_step / 3.0
        
        try:
            fa = float(f_lam(a))
        except TypeError:
            fa = float(f_lam())
            
        if abs(K) < 1e-12:
            rhs = fa * (b - a)
        else:
            try:
                rhs = fa * (math.exp(K * (b - a)) - 1) / K
            except OverflowError:
                rhs = float('inf')
        neg_q = integral_val > rhs + 1e-7
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a strictly positive, continuously differentiable real-valued function on the interval a to b",
    "¬Q: Integral of f(x) from a to b > f(a) * (exp(K*(b-a)) - 1) / K"
]

N_HYP = 1
NEG_Q_INDEX = 1