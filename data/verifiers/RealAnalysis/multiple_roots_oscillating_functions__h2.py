import sympy
from sympy.abc import x
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        f = sympy.sympify(witness['f'])
        a = float(witness['a'])
        b = float(witness['b'])
        k = int(witness['k'])
        
        if 'X' in witness:
            X = witness['X']
        elif 'x' in witness:
            X = witness['x']
        elif 'x_i' in witness:
            X = witness['x_i']
        else:
            X = witness.get('x_list', [])
            
        if not X:
            return [False, False, False]
            
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
        else:
            sym = x
            
    except Exception:
        return [False, False, False]

    # H1: f is continuous on the interval
    h1_ok = False
    try:
        if a <= b:
            # Check denominator for roots in the interval
            num, den = f.as_numer_denom()
            den_roots = sympy.solve(den, sym)
            den_ok = True
            for r in den_roots:
                try:
                    rf = float(r)
                    if a <= rf <= b:
                        den_ok = False
                        break
                except TypeError:
                    pass
            
            if den_ok:
                # Check a few points to ensure real values
                pts_ok = True
                step = (b - a) / 50.0
                for i in range(51):
                    val = a + i * step
                    y = f.subs(sym, val)
                    try:
                        yf = float(y)
                    except TypeError:
                        pts_ok = False
                        break
                if pts_ok:
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H2: f(x_i) * f(x_{i+1}) < 0 for i=1..k-1
    h2_ok = False
    try:
        if len(X) == k and k >= 2:
            all_in_domain = True
            for xi in X:
                if not (a <= float(xi) <= b):
                    all_in_domain = False
                    break
            if all_in_domain:
                products_negative = True
                for i in range(k - 1):
                    y1 = float(f.subs(sym, X[i]))
                    y2 = float(f.subs(sym, X[i+1]))
                    if y1 * y2 >= 0:
                        products_negative = False
                        break
                if products_negative:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: f has fewer than k-1 distinct roots in the interval
    neg_q_ok = False
    try:
        valid_roots = set()
        try:
            sol = sympy.solveset(f, sym, domain=sympy.S.Reals)
            if isinstance(sol, sympy.FiniteSet):
                for r in sol:
                    try:
                        rf = float(r)
                        if a < rf < b:
                            valid_roots.add(round(rf, 9))
                    except TypeError:
                        pass
            else:
                raise ValueError("Not a FiniteSet")
        except Exception:
            # Fallback to solve if solveset fails or returns non-FiniteSet
            roots = sympy.solve(f, sym)
            for r in roots:
                try:
                    rf = float(r)
                    if a < rf < b:
                        valid_roots.add(round(rf, 9))
                except TypeError:
                    pass
        
        num_roots = len(valid_roots)
        if num_roots < k - 1:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a continuous function on the interval",
    "H_2: f(x_i) * f(x_i+1) < 0 for all integers i from 1 to k-1",
    "¬Q: f has fewer than k-1 distinct roots in the interval"
]

N_HYP = 2
NEG_Q_INDEX = 2