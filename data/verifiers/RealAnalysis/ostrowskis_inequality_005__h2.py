import sympy as sp
import math

x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is continuous and differentiable",
    "not Q: Ostrowski inequality fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = sp.sympify(witness['f'])
            a = float(witness['a'])
            b = float(witness['b'])
            M = float(witness['M'])
        else:
            f, a, b, M = witness
            f = sp.sympify(f)
            a = float(a)
            b = float(b)
            M = float(M)
    except Exception:
        return [False, False]
        
    h1_ok = False
    try:
        if a < b:
            f_lam = sp.lambdify(x, f, modules=['math'])
            df = sp.diff(f, x)
            df_lam = sp.lambdify(x, df, modules=['math'])
            
            h1_ok = True
            # Check continuity
            for i in range(51):
                p = a + (b - a) * i / 50.0
                try:
                    val = float(f_lam(p))
                    if math.isnan(val) or math.isinf(val):
                        h1_ok = False
                        break
                except Exception:
                    h1_ok = False
                    break
                    
            # Check differentiability
            if h1_ok:
                for i in range(1, 50):
                    p = a + (b - a) * i / 50.0
                    try:
                        val = float(df_lam(p))
                        if math.isnan(val) or math.isinf(val):
                            h1_ok = False
                            break
                    except Exception:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False
        
    neg_q_ok = False
    try:
        if h1_ok:
            try:
                t = sp.Symbol('t', real=True)
                integral_expr = sp.integrate(f.subs(x, t), (t, a, b))
                if not integral_expr.has(sp.Integral):
                    integral_val = float(integral_expr.evalf())
                else:
                    raise ValueError("Unevaluated integral")
            except Exception:
                # Simpson's rule for integral
                N = 1000
                h = (b - a) / N
                s = float(f_lam(a)) + float(f_lam(b))
                for i in range(1, N, 2):
                    s += 4 * float(f_lam(a + i * h))
                for i in range(2, N-1, 2):
                    s += 2 * float(f_lam(a + i * h))
                integral_val = s * h / 3.0
            
            avg_f = integral_val / (b - a)
            
            pts = [a + (b - a) * i / 1000.0 for i in range(1001)]
            for p in pts:
                try:
                    lhs = abs(float(f_lam(p)) - avg_f)
                    rhs = M * (b - a) * (0.25 + ((p - (a + b) / 2.0) ** 2) / ((b - a) ** 2))
                    if lhs > rhs + 1e-7:
                        neg_q_ok = True
                        break
                except Exception:
                    pass
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]