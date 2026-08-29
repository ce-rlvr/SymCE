import sympy as sp
from sympy.abc import x
from sympy.calculus.util import continuous_domain
import math

def conditions(witness):
    """
    witness is a tuple: (f, a, b)
    where f is a sympy expression in terms of x
    and a and b are real numbers.
    """
    try:
        f, a, b = witness
        _ = float(a)
        _ = float(b)
    except Exception:
        return [False, False]

    def check_h1():
        try:
            if float(a) > float(b):
                return True
            
            f1 = sp.diff(f, x)
            f2 = sp.diff(f1, x)
            
            if float(a) == float(b):
                v0 = f.subs(x, a)
                v1 = f1.subs(x, a)
                v2 = f2.subs(x, a)
                try:
                    float(v0); float(v1); float(v2)
                    return True
                except Exception:
                    return False

            interval = sp.Interval(a, b)
            
            cd_f = continuous_domain(f, x, sp.Reals)
            if not interval.is_subset(cd_f): return False
            
            cd_f1 = continuous_domain(f1, x, sp.Reals)
            if not interval.is_subset(cd_f1): return False
            
            cd_f2 = continuous_domain(f2, x, sp.Reals)
            if not interval.is_subset(cd_f2): return False
            
            return True
        except Exception:
            try:
                f1 = sp.diff(f, x)
                f2 = sp.diff(f1, x)
                n_points = 100
                a_f = float(a)
                b_f = float(b)
                for i in range(n_points + 1):
                    val = a_f + i * (b_f - a_f) / n_points
                    v = f2.subs(x, val)
                    try:
                        float(v)
                    except Exception:
                        return False
                return True
            except Exception:
                return False

    def check_conclusion():
        try:
            if float(a) >= float(b):
                return False
            
            integral = sp.integrate(f, (x, a, b))
            trapz = (f.subs(x, a) + f.subs(x, b)) / 2 * (b - a)
            LHS = sp.simplify(integral - trapz)
            
            f2 = sp.diff(f, x, 2)
            target_f2 = sp.simplify(-12 * LHS / (b - a)**3)
            
            if f2.is_constant():
                diff_val = sp.simplify(f2 - target_f2)
                if diff_val == 0:
                    return True
                try:
                    if abs(float(diff_val)) < 1e-9:
                        return True
                except Exception:
                    pass
                return False
                
            c = sp.Symbol('c', real=True)
            eq = sp.Eq(f2.subs(x, c), target_f2)
            sols = sp.solve(eq, c)
            for sol in sols:
                try:
                    sol_f = float(sol)
                    if float(a) < sol_f < float(b):
                        return True
                except Exception:
                    pass
            
            try:
                target_val = float(target_f2)
                vals = []
                a_f = float(a)
                b_f = float(b)
                for i in range(1, 1000):
                    cv = a_f + i * (b_f - a_f) / 1000
                    vals.append(float(f2.subs(x, cv)))
                if min(vals) - 1e-9 <= target_val <= max(vals) + 1e-9:
                    return True
            except Exception:
                pass
                
            return False
        except Exception:
            return False

    h1_ok = False
    try:
        h1_ok = check_h1()
    except Exception:
        pass
        
    neg_q_ok = False
    try:
        neg_q_ok = not check_conclusion()
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is twice continuously differentiable on the interval a to b",
    "¬Q: There does not exist c in the interval a to b satisfying the error formula"
]

N_HYP = 1
NEG_Q_INDEX = 1