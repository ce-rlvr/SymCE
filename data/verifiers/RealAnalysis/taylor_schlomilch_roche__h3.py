import sympy
from sympy import diff, Symbol, Interval, Eq, solve
import math

# Top-level setup
x = Symbol('x', real=True)

def check_continuous(expr, var, a, b):
    try:
        from sympy.calculus.util import continuous_domain
        domain = continuous_domain(expr, var, sympy.S.Reals)
        if Interval(a, b).is_subset(domain):
            return True
    except Exception:
        pass
    
    # Fallback: evaluate at 101 points in the interval
    try:
        a_f = float(a)
        b_f = float(b)
        for i in range(101):
            v = a_f + (b_f - a_f) * i / 100.0
            val = expr.subs(var, v)
            val_f = float(val)
            if math.isnan(val_f) or math.isinf(val_f):
                return False
        return True
    except Exception:
        return False

def check_continuous_open(expr, var, a, b):
    try:
        from sympy.calculus.util import continuous_domain
        domain = continuous_domain(expr, var, sympy.S.Reals)
        if Interval.open(a, b).is_subset(domain):
            return True
    except Exception:
        pass
    
    # Fallback: evaluate at 99 points in the open interval
    try:
        a_f = float(a)
        b_f = float(b)
        for i in range(1, 100):
            v = a_f + (b_f - a_f) * i / 100.0
            val = expr.subs(var, v)
            val_f = float(val)
            if math.isnan(val_f) or math.isinf(val_f):
                return False
        return True
    except Exception:
        return False

def is_valid_n(n):
    try:
        return int(n) == n and int(n) >= 0
    except Exception:
        return False

def conditions(witness):
    """
    witness: tuple (f, a, b, n, p)
    where f is a sympy expression in terms of x,
    a, b are real numbers with a < b,
    n is a non-negative integer,
    p is a real number.
    """
    try:
        if len(witness) != 5:
            return [False, False, False]
        f, a, b, n, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: f is n times continuously differentiable
    try:
        if not (a < b) or not is_valid_n(n):
            h1 = False
        else:
            fn = diff(f, x, int(n))
            h1 = check_continuous(fn, x, a, b)
    except Exception:
        h1 = False

    # H_2: The (n+1)-th derivative exists
    try:
        if not (a < b) or not is_valid_n(n):
            h2 = False
        else:
            fn1 = diff(f, x, int(n) + 1)
            h2 = check_continuous_open(fn1, x, a, b)
    except Exception:
        h2 = False

    # neg_Q: There is NO c satisfying the remainder formula
    try:
        if not (a < b) or not is_valid_n(n):
            neg_q = False
        elif p == 0:
            # The formula has p in the denominator, so it's undefined (fails) for p=0
            neg_q = True
        else:
            n_int = int(n)
            # Calculate the actual remainder R_n(b)
            R_n_b = f.subs(x, b) - sum(diff(f, x, k).subs(x, a) / math.factorial(k) * (b - a)**k for k in range(n_int + 1))
            
            c = Symbol('c', real=True)
            fn1 = diff(f, x, n_int + 1)
            fn1_c = fn1.subs(x, c)
            
            # Schlomilch-Roche remainder formula RHS
            rhs = fn1_c / (math.factorial(n_int) * p) * (b - c)**(n_int + 1 - p) * (b - a)**p
            
            eq = Eq(R_n_b, rhs)
            sols = solve(eq, c)
            
            has_sol = False
            if isinstance(sols, list):
                for sol in sols:
                    val = sol[c] if isinstance(sol, dict) and c in sol else sol
                    try:
                        sol_val = complex(val)
                        if abs(sol_val.imag) < 1e-9 and float(a) < sol_val.real < float(b):
                            has_sol = True
                            break
                    except Exception:
                        try:
                            sol_f = float(val.evalf())
                            if float(a) < sol_f < float(b):
                                has_sol = True
                                break
                        except Exception:
                            pass
            elif isinstance(sols, dict):
                if c in sols:
                    val = sols[c]
                    try:
                        sol_val = complex(val)
                        if abs(sol_val.imag) < 1e-9 and float(a) < sol_val.real < float(b):
                            has_sol = True
                    except Exception:
                        pass
            
            # Numerical fallback if exact solve fails or returns empty
            if not has_sol:
                g = rhs - R_n_b
                g_vals = []
                for i in range(1, 1000):
                    cv = float(a) + (float(b) - float(a)) * i / 1000.0
                    try:
                        gv = float(g.subs(c, cv))
                        if math.isnan(gv) or math.isinf(gv):
                            continue
                        g_vals.append(gv)
                        if abs(gv) < 1e-7:
                            has_sol = True
                            break
                    except Exception:
                        pass
                
                if not has_sol and g_vals:
                    # If the continuous function g changes sign, there is a root by IVT
                    if max(g_vals) > 0 and min(g_vals) < 0:
                        has_sol = True
                        
            neg_q = not has_sol
    except Exception:
        # If evaluating the conclusion raises an error, the formula is invalid, so conclusion fails
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is n times continuously differentiable",
    "H_2: The n+1 th derivative exists",
    "¬Q: There is no c satisfying the remainder formula"
]

N_HYP = 2
NEG_Q_INDEX = 2