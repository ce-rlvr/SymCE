import sympy
from sympy import Symbol, Interval, S, solveset, simplify, diff

# Top-level setup
x = Symbol('x')
y = Symbol('y')

def conditions(witness):
    try:
        f, a, b = witness
    except Exception:
        return [False, False, False]
    
    try:
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = Symbol('x')
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: f is continuous on the closed interval from a to b
    try:
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        if not (a.is_real and b.is_real and a < b):
            h1 = False
        else:
            if hasattr(sympy, 'continuous_domain'):
                dom = sympy.continuous_domain(f, var, S.Reals)
            else:
                from sympy.calculus.util import continuous_domain
                dom = continuous_domain(f, var, S.Reals)
            h1 = bool(Interval(a, b).is_subset(dom))
    except Exception:
        h1 = False

    # H2: f(a) == f(b)
    try:
        val_a = f.subs(var, a)
        val_b = f.subs(var, b)
        h2 = bool(simplify(val_a - val_b) == 0)
    except Exception:
        h2 = False

    # neg_Q: NO point c in the open interval where the derivative is 0
    try:
        f_prime = diff(f, var)
        sols = solveset(f_prime, var, domain=Interval.open(a, b))
        
        if sols.is_empty == True:
            neg_q = True
        elif sols.is_empty == False:
            if isinstance(sols, sympy.FiniteSet):
                has_stat_point = False
                for c in sols:
                    try:
                        # Verify using the limit of the difference quotient to avoid false positives 
                        # from SymPy's formal derivatives at points of non-differentiability (e.g., Abs(x) at 0)
                        h = Symbol('h', real=True)
                        diff_quotient = (f.subs(var, c + h) - f.subs(var, c)) / h
                        lim_left = sympy.limit(diff_quotient, h, 0, dir='-')
                        lim_right = sympy.limit(diff_quotient, h, 0, dir='+')
                        if simplify(lim_left) == 0 and simplify(lim_right) == 0:
                            has_stat_point = True
                            break
                    except Exception:
                        pass
                neg_q = not has_stat_point
            else:
                # If it's an interval or union containing an interval, it has stationary points
                neg_q = False
        else:
            # ConditionSet or unable to determine
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on the closed interval from a to b",
    "H_2: f(a) = f(b)",
    "¬Q: There is no point c between a and b such that the derivative is 0"
]

N_HYP = 2
NEG_Q_INDEX = 2