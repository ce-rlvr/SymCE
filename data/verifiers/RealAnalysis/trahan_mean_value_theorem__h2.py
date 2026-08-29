import sympy
from sympy import Symbol, solveset, S, Interval, diff
import math

# Top-level setup
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is differentiable on the interval",
    "H_2: The difference quotient lies strictly between f'(a) and f'(b)",
    "¬Q: There is no c in the interval such that f(c) - f(a) = (c-a)f'(c)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        f, a, b = witness
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False]
    
    # H_1: f is differentiable on the interval
    try:
        if not bool(a < b):
            h1 = False
        else:
            df = diff(f, x)
            h1 = True
            
            # Check for known singularities in the interval
            try:
                from sympy.calculus.singularities import singularities
                sings = singularities(df, x)
                if sings.intersect(Interval(a, b)).is_empty == False:
                    h1 = False
            except Exception:
                pass
            
            # Heuristic check at multiple points
            if h1:
                pts = [a + i*(b-a)/10 for i in range(11)]
                for p in pts:
                    val = df.subs(x, p)
                    try:
                        val_num = complex(val)
                        if abs(val_num.imag) > 1e-9 or math.isnan(val_num.real) or math.isinf(val_num.real):
                            h1 = False
                            break
                    except Exception:
                        if val.has(sympy.oo, sympy.zoo, -sympy.oo, sympy.nan):
                            h1 = False
                            break
    except Exception:
        h1 = False

    # H_2: The difference quotient lies strictly between f'(a) and f'(b)
    try:
        df = diff(f, x)
        fa = f.subs(x, a)
        fb = f.subs(x, b)
        dfa = df.subs(x, a)
        dfb = df.subs(x, b)
        q = (fb - fa) / (b - a)
        
        dfa_num = float(dfa)
        dfb_num = float(dfb)
        q_num = float(q)
        
        cond1 = (dfa_num < q_num) and (q_num < dfb_num)
        cond2 = (dfb_num < q_num) and (q_num < dfa_num)
        h2 = cond1 or cond2
    except Exception:
        h2 = False

    # ¬Q: There is no c in the interval such that f(c) - f(a) = (c-a)f'(c)
    try:
        df = diff(f, x)
        fa = f.subs(x, a)
        eq = f - fa - (x - a)*df
        
        roots = solveset(eq, x, domain=Interval.open(a, b))
        if roots == sympy.EmptySet:
            neg_q = True
        elif isinstance(roots, sympy.FiniteSet):
            neg_q = len(roots) == 0
        else:
            # Fallback to solve if solveset returns a ConditionSet or complex structure
            sols = sympy.solve(eq, x, dict=True)
            neg_q = True
            for sol_dict in sols:
                if x in sol_dict:
                    sol = sol_dict[x]
                    # Numeric check
                    try:
                        sol_num = complex(sol)
                        if abs(sol_num.imag) < 1e-9:
                            if float(a) < sol_num.real < float(b):
                                neg_q = False
                                break
                    except Exception:
                        pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]