import sympy
from sympy import Symbol, Interval, oo, zoo
from sympy.calculus.util import function_range
import math

x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

CONDITION_LABELS = [
    "H_1: I is a closed and bounded interval in R",
    "¬Q: f is not bounded on I"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f', witness.get('func'))
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, a, b = witness
    except Exception:
        return [False, False]

    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        if a_sym.is_real and b_sym.is_real and a_sym.is_finite and b_sym.is_finite:
            h1 = bool(a_sym <= b_sym)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if callable(f):
            f_sym = f(x)
        else:
            f_sym = sympy.sympify(f)
    except Exception:
        f_sym = f

    try:
        free_syms = getattr(f_sym, "free_symbols", set())
        if x in free_syms:
            var = x
        elif free_syms:
            var = list(free_syms)[0]
        else:
            var = x
        
        rng = function_range(f_sym, var, Interval(a_sym, b_sym))
        neg_q = bool(rng.sup == oo or rng.inf == -oo)
    except Exception:
        try:
            from sympy.calculus.singularities import singularities
            sings = singularities(f_sym, var, Interval(a_sym, b_sym))
            if sings and not sings.is_empty:
                neg_q = True
            else:
                raise ValueError("Fallback to evaluation")
        except Exception:
            try:
                neg_q = False
                a_f = float(a_sym)
                b_f = float(b_sym)
                pts = [a_f + (b_f - a_f) * i / 1000.0 for i in range(1001)]
                pts += [a_f + 1e-9, b_f - 1e-9, a_f + 1e-6, b_f - 1e-6]
                for pt in pts:
                    try:
                        val = f_sym.subs(var, pt)
                        if val.has(oo, zoo, -oo):
                            neg_q = True
                            break
                        if abs(float(val)) > 1e6:
                            neg_q = True
                            break
                    except Exception:
                        pass
            except Exception:
                neg_q = False

    return [h1, neg_q]