import sympy as sp
from sympy.abc import x
import math

# Top-level setup
# x is imported from sympy.abc and serves as the variable for the function expressions.

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks if it is a valid counterexample.
    The witness should be a tuple (f, a, b) or a dictionary with keys "f", "a", "b",
    where f is a sympy expression in terms of x, and a, b are real numbers.
    """
    try:
        if isinstance(witness, dict):
            f = witness.get("f")
            a = witness.get("a")
            b = witness.get("b")
        else:
            f, a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: f is defined on [a, b]
    try:
        h1 = True
        if float(a) >= float(b):
            h1 = False
        else:
            v_a = f.subs(x, a)
            v_b = f.subs(x, b)
            
            def is_valid_real(val):
                try:
                    fval = float(val)
                    return not (math.isinf(fval) or math.isnan(fval))
                except Exception:
                    return False

            if not is_valid_real(v_a) or not is_valid_real(v_b):
                h1 = False
            
            v_mid = f.subs(x, (a+b)/2)
            if not is_valid_real(v_mid):
                h1 = False

            # Check for known singularities in [a, b]
            try:
                sings = sp.singularities(f, x)
                if isinstance(sings, sp.Set):
                    inter = sp.Intersection(sings, sp.Interval(a, b))
                    if not inter.is_empty:
                        h1 = False
            except Exception:
                pass
            
            # Check for denominators and undefined domains in f
            for subexpr in sp.preorder_traversal(f):
                if subexpr.is_Pow and subexpr.exp < 0:
                    sols = sp.solveset(subexpr.base, x, domain=sp.Interval(a, b))
                    if not sols.is_empty:
                        h1 = False
                elif subexpr.func == sp.log:
                    sols = sp.solveset(subexpr.args[0] <= 0, x, domain=sp.Interval(a, b))
                    if not sols.is_empty:
                        h1 = False
                elif subexpr.func in (sp.tan, sp.sec):
                    sols = sp.solveset(sp.cos(subexpr.args[0]), x, domain=sp.Interval(a, b))
                    if not sols.is_empty:
                        h1 = False
                elif subexpr.func in (sp.cot, sp.csc):
                    sols = sp.solveset(sp.sin(subexpr.args[0]), x, domain=sp.Interval(a, b))
                    if not sols.is_empty:
                        h1 = False
    except Exception:
        h1 = False

    # H_2: f is differentiable on (a, b)
    try:
        h2 = True
        df = f.diff(x)
        
        # Check for denominators and undefined domains in df
        for subexpr in sp.preorder_traversal(df):
            if subexpr.is_Pow and subexpr.exp < 0:
                sols = sp.solveset(subexpr.base, x, domain=sp.Interval.open(a, b))
                if not sols.is_empty:
                    h2 = False
            elif subexpr.func == sp.log:
                sols = sp.solveset(subexpr.args[0] <= 0, x, domain=sp.Interval.open(a, b))
                if not sols.is_empty:
                    h2 = False
            elif subexpr.func in (sp.tan, sp.sec):
                sols = sp.solveset(sp.cos(subexpr.args[0]), x, domain=sp.Interval.open(a, b))
                if not sols.is_empty:
                    h2 = False
            elif subexpr.func in (sp.cot, sp.csc):
                sols = sp.solveset(sp.sin(subexpr.args[0]), x, domain=sp.Interval.open(a, b))
                if not sols.is_empty:
                    h2 = False

        # Check piecewise boundaries for continuity and differentiability
        f_pw = f.rewrite(sp.Piecewise)
        df_pw = df.rewrite(sp.Piecewise)
        points_to_check = set()
        for expr in list(f_pw.atoms(sp.Relational)) + list(df_pw.atoms(sp.Relational)):
            if expr.has(x):
                eq = sp.Eq(expr.lhs, expr.rhs)
                sols = sp.solveset(eq, x, domain=sp.S.Reals)
                if isinstance(sols, sp.FiniteSet):
                    for sol in sols:
                        if sol.is_real and a < sol < b:
                            points_to_check.add(sol)
                            
        for pt in points_to_check:
            l_f = sp.limit(f, x, pt, dir="-")
            r_f = sp.limit(f, x, pt, dir="+")
            v_f = f.subs(x, pt)
            if l_f != v_f or r_f != v_f:
                h2 = False
                break
            
            l_df = sp.limit(df, x, pt, dir="-")
            r_df = sp.limit(df, x, pt, dir="+")
            if l_df != r_df:
                h2 = False
                break
                
            try:
                fval = float(l_df)
                if math.isinf(fval) or math.isnan(fval):
                    h2 = False
                    break
            except Exception:
                h2 = False
                break
                
        # Check for known singularities in df
        try:
            sings_df = sp.singularities(df, x)
            if isinstance(sings_df, sp.Set) and not sp.Intersection(sings_df, sp.Interval.open(a, b)).is_empty:
                h2 = False
        except Exception:
            pass

        # Sample points evaluation
        if h2:
            for i in range(1, 10):
                pt = a + i * (b - a) / 10.0
                val = df.subs(x, pt)
                try:
                    fval = float(val)
                    if math.isinf(fval) or math.isnan(fval):
                        h2 = False
                        break
                except Exception:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # not Q: There is no c in (a, b) such that df(c) = (f(b) - f(a)) / (b - a)
    try:
        v_a = f.subs(x, a)
        v_b = f.subs(x, b)
        target = (v_b - v_a) / (b - a)
        eq = sp.Eq(df, target)
        sols = sp.solveset(eq, x, domain=sp.Interval.open(a, b))
        if sols.is_empty:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = ["H_1: f is defined on a closed interval", "H_2: f is differentiable on the open interval", "not Q: conclusion fails"]
N_HYP = 2
NEG_Q_INDEX = 2