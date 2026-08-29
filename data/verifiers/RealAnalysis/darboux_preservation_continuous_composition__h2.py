import sympy as sp
from sympy import Symbol, S, Interval, solveset, Piecewise
from sympy.calculus.util import continuous_domain
from sympy.calculus.singularities import singularities
import math
import itertools
import functools

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness can be either:
      - A tuple (f, g, I)
      - A tuple (f, g, I, a, b, y)
    where f and g are SymPy expressions (or callables) in terms of x,
    I is a SymPy Interval, a and b are points in I, and y is a value strictly between
    (g o f)(a) and (g o f)(b) that is not attained by g o f on the interval between a and b.
    """
    try:
        if len(witness) == 6:
            f, g, I, a, b, y = witness
            candidates = [(a, b, y)]
        elif len(witness) == 3:
            f, g, I = witness
            candidates = None
        else:
            return [False, False, False]
            
        if callable(f):
            f = f(x)
        if callable(g):
            g = g(x)
    except Exception:
        return [False, False, False]

    # H1: f is a real-valued function defined on an interval I
    try:
        h1 = bool(isinstance(I, sp.Interval) and isinstance(f, sp.Expr))
        if h1:
            try:
                sings = singularities(f, x, I)
                if isinstance(sings, sp.Set) and not isinstance(sings, sp.ConditionSet):
                    if sings != sp.S.EmptySet:
                        h1 = False
            except Exception:
                pass
    except Exception:
        h1 = False

    # H2: g is a real-valued continuous function defined on R
    try:
        dom = continuous_domain(g, x, sp.S.Reals)
        h2 = bool(dom == sp.S.Reals)
    except Exception:
        h2 = False

    # Negated Conclusion: g o f does NOT have the intermediate value property on I
    try:
        h_expr = g.subs(x, f)
        
        if candidates is None:
            points = []
            if I.start.is_finite and I.end.is_finite:
                start, end = I.start, I.end
                points = [start + (end - start) * sp.Rational(i, 10) for i in range(11)]
            else:
                start = I.start if I.start.is_finite else -10
                end = I.end if I.end.is_finite else 10
                points = [sp.Rational(i, 1) for i in range(int(start), int(end)+1) if I.contains(i) == True]
            
            candidates = []
            for i in range(len(points)):
                for j in range(i+1, len(points)):
                    a_val = points[i]
                    b_val = points[j]
                    if I.contains(a_val) != True or I.contains(b_val) != True:
                        continue
                    ha = h_expr.subs(x, a_val)
                    hb = h_expr.subs(x, b_val)
                    if ha.is_real == True and hb.is_real == True and ha != hb:
                        y_val = (ha + hb) / 2
                        candidates.append((a_val, b_val, y_val))

        neg_q = False
        for a_val, b_val, y_val in candidates:
            if I.contains(a_val) != True or I.contains(b_val) != True:
                continue
            ha = h_expr.subs(x, a_val)
            hb = h_expr.subs(x, b_val)
            if ha == hb:
                continue
            
            # y_val must be strictly between ha and hb
            if not ((ha < y_val and y_val < hb) or (hb < y_val and y_val < ha)):
                continue
            
            interval_ab = sp.Interval(min(a_val, b_val), max(a_val, b_val))
            sols = sp.solveset(h_expr - y_val, x, domain=interval_ab)
            
            if sols == sp.S.EmptySet:
                neg_q = True
                break
            
            # Fallback if solveset returns a ConditionSet (common with Piecewise)
            if isinstance(sols, sp.ConditionSet):
                if isinstance(h_expr, sp.Piecewise):
                    values = [arg[0] for arg in h_expr.args]
                    if all(v.is_constant() for v in values):
                        if all(y_val != v for v in values):
                            neg_q = True
                            break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]


CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on an interval I",
    "H_2: g is a real-valued continuous function defined on R",
    "¬Q: g ∘ f does not have the intermediate value property on I"
]

N_HYP = 2
NEG_Q_INDEX = 2