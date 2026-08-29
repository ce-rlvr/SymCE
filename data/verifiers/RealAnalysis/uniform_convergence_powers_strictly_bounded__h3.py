import sympy
from sympy import Symbol, maximum, Abs, Expr, Set, Interval, Reals
import math
import itertools
import functools

# Top-level setup for potential witness expressions
x = Symbol('x', real=True)

def conditions(witness):
    try:
        S, f = witness
    except Exception:
        return [False, False, False]

    # H1: S is an arbitrary set
    try:
        if isinstance(S, Set):
            h1 = True
        else:
            iter(S)
            h1 = True
    except Exception:
        h1 = False

    # H2: f is a real-valued function on S
    try:
        h2 = False
        is_iterable = False
        try:
            iter(S)
            is_iterable = True
        except TypeError:
            pass

        if is_iterable:
            h2 = True
            for pt in S:
                if callable(f):
                    val = f(pt)
                else:
                    syms = list(f.free_symbols)
                    val = f.subs(syms[0], pt) if syms else f
                if complex(val).imag != 0:
                    h2 = False
                    break
        else:
            if callable(f) or hasattr(f, 'free_symbols'):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: f_n(x) = (f(x))^n does NOT converge uniformly to 0 on S
    # This is equivalent to sup_{x \in S} |f(x)| >= 1
    try:
        neg_q = False
        is_iterable = False
        try:
            iter(S)
            is_iterable = True
        except TypeError:
            pass

        if is_iterable:
            for pt in S:
                if callable(f):
                    val = f(pt)
                else:
                    syms = list(f.free_symbols)
                    val = f.subs(syms[0], pt) if syms else f
                if abs(complex(val)) >= 1:
                    neg_q = True
                    break
        else:
            x_sym = Symbol('x', real=True)
            expr = None
            if callable(f):
                try:
                    expr = f(x_sym)
                    if not hasattr(expr, 'free_symbols'):
                        expr = sympy.sympify(expr)
                except Exception:
                    # Fallback to sampling if f cannot handle symbolic input
                    if hasattr(S, 'inf') and hasattr(S, 'sup'):
                        inf = float(S.inf) if S.inf.is_real else -10.0
                        sup = float(S.sup) if S.sup.is_real else 10.0
                        for i in range(101):
                            pt = inf + (sup - inf) * i / 100.0
                            try:
                                if abs(complex(f(pt))) >= 1:
                                    neg_q = True
                                    break
                            except Exception:
                                pass
            else:
                expr = f
            
            if expr is not None:
                if isinstance(expr, (int, float, complex)) or (hasattr(expr, 'is_number') and expr.is_number):
                    if abs(complex(expr)) >= 1:
                        neg_q = True
                else:
                    syms = list(expr.free_symbols)
                    if syms:
                        var = syms[0]
                        try:
                            sup_val = maximum(Abs(expr), var, S)
                            if sup_val >= 1:
                                neg_q = True
                        except Exception:
                            # Fallback to sampling if maximum fails
                            if hasattr(S, 'inf') and hasattr(S, 'sup'):
                                inf = float(S.inf) if S.inf.is_real else -10.0
                                sup = float(S.sup) if S.sup.is_real else 10.0
                                for i in range(101):
                                    pt = inf + (sup - inf) * i / 100.0
                                    try:
                                        val = expr.subs(var, pt)
                                        if abs(complex(val)) >= 1:
                                            neg_q = True
                                            break
                                    except Exception:
                                        pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is an arbitrary set",
    "H_2: f is a real-valued function on S",
    "¬Q: The sequence of functions f_n(x) = (f(x))^n does not converge uniformly to the zero function on S"
]

N_HYP = 2
NEG_Q_INDEX = 2