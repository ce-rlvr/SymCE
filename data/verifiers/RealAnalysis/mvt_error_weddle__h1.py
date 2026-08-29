import sympy as sp
from sympy import Symbol, diff, integrate, solveset, S, Interval
from sympy.calculus.util import continuous_domain
import math

x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            h = witness.get('h', (b - a) / 6)
        else:
            if len(witness) == 3:
                f, a, b = witness
                h = (b - a) / 6
            else:
                f, a, b, h = witness
    except Exception:
        return [False, False, False]
        
    try:
        if callable(f):
            f_expr = f(x)
            var = x
        else:
            f_expr = sp.sympify(f)
            free = f_expr.free_symbols
            for param in (a, b, h):
                if isinstance(param, Symbol):
                    free.discard(param)
            var = list(free)[0] if free else x
            
        f6 = diff(f_expr, var, 6)
        
        if f6.is_polynomial(var):
            h1 = bool(a < b)
        else:
            dom = continuous_domain(f6, var, Interval(a, b))
            h1 = bool(Interval(a, b).is_subset(dom)) and bool(a < b)
    except Exception:
        h1 = False

    try:
        diff_h = sp.simplify(h - (b - a) / 6)
        try:
            h2 = bool(diff_h == 0 or abs(float(diff_h)) < 1e-9)
        except Exception:
            h2 = bool(diff_h == 0)
    except Exception:
        h2 = False

    try:
        I_exact = integrate(f_expr, (var, a, b))
        
        W = 3 * h / 10 * (
            f_expr.subs(var, a) + 
            5 * f_expr.subs(var, a + h) + 
            f_expr.subs(var, a + 2 * h) + 
            6 * f_expr.subs(var, a + 3 * h) + 
            f_expr.subs(var, a + 4 * h) + 
            5 * f_expr.subs(var, a + 5 * h) + 
            f_expr.subs(var, b)
        )
        
        E = sp.simplify(I_exact - W)
        target = sp.simplify(- (h**7 / 140) * f6)
        eq = sp.simplify(target - E)
        
        if eq.is_constant():
            try:
                is_z = bool(eq == 0 or abs(float(eq)) < 1e-9)
            except Exception:
                is_z = bool(eq.is_zero)
            if is_z:
                neg_q = False
            else:
                neg_q = True
        else:
            roots = solveset(eq, var, domain=S.Reals)
            if roots is S.EmptySet:
                neg_q = True
            elif isinstance(roots, sp.FiniteSet):
                has_root_in_interval = False
                for r in roots:
                    try:
                        if r.is_real is False:
                            continue
                        r_float = float(r)
                        if float(a) < r_float < float(b):
                            has_root_in_interval = True
                            break
                    except Exception:
                        try:
                            if a < r < b:
                                has_root_in_interval = True
                                break
                        except Exception:
                            pass
                neg_q = not has_root_in_interval
            else:
                n_samples = 100
                vals = []
                for i in range(1, n_samples):
                    pt = a + (b - a) * i / n_samples
                    try:
                        val = float(eq.subs(var, pt))
                        vals.append(val)
                    except Exception:
                        pass
                if not vals:
                    neg_q = False
                else:
                    pos = all(v > 1e-9 for v in vals)
                    neg = all(v < -1e-9 for v in vals)
                    min_abs = min(abs(v) for v in vals)
                    if (pos or neg) and min_abs > 1e-5:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is continuous on the interval",
    "H_2: h is equal to b minus a over 6",
    "not Q: there is no c in the interval satisfying the equation"
]

N_HYP = 2
NEG_Q_INDEX = 2