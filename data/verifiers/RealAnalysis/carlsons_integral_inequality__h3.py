import sympy
from sympy import Symbol, singularities, Interval, oo, fraction, solve, integrate, zoo, nan
from sympy.abc import x
import math
import itertools
import functools

# Top-level setup
# x is provided from sympy.abc for witness expressions to reference

def conditions(witness):
    h1_ok = False
    try:
        free_symbols = witness.free_symbols
        if len(free_symbols) == 0:
            try:
                c = complex(witness)
                h1_ok = (abs(c.imag) <= 1e-5 and c.real >= -1e-9)
            except Exception:
                h1_ok = False
        elif len(free_symbols) == 1:
            sym = list(free_symbols)[0]
            f = witness
            h1_ok = True
            
            # Check non-negativity at sample points
            for val in [0.0, 0.5, 1.0, 2.0, 10.0, 100.0]:
                try:
                    v = complex(f.subs(sym, val))
                    if abs(v.imag) > 1e-5 or v.real < -1e-9:
                        h1_ok = False
                        break
                except Exception:
                    pass
                    
            if h1_ok:
                # Check that value at 0 is finite
                try:
                    v0 = f.subs(sym, 0)
                    if v0.has(oo, zoo, nan, -oo):
                        h1_ok = False
                except Exception:
                    pass

            if h1_ok:
                # Check continuity on [0, oo)
                try:
                    sings = singularities(f, sym)
                    if not sings.intersect(Interval(0, oo)).is_empty:
                        h1_ok = False
                except Exception:
                    # Fallback: check roots of the denominator
                    try:
                        n, d = fraction(f)
                        roots = solve(d, sym)
                        for r in roots:
                            if r.is_real and r >= 0:
                                h1_ok = False
                                break
                    except Exception:
                        pass
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        free_symbols = witness.free_symbols
        if len(free_symbols) == 0:
            try:
                c = complex(witness)
                # Integral of a non-zero constant over [0, oo) diverges
                h2_ok = (abs(c.imag) <= 1e-5 and abs(c.real) <= 1e-9)
            except Exception:
                h2_ok = False
        elif len(free_symbols) == 1:
            sym = list(free_symbols)[0]
            f = witness
            I2 = integrate(f**2, (sym, 0, oo))
            
            def is_conv(I):
                if I.has(oo, zoo, nan, -oo):
                    return False
                try:
                    c = complex(I)
                    return abs(c.imag) <= 1e-5
                except Exception:
                    try:
                        v = I.evalf()
                        if v.has(oo, zoo, nan, -oo):
                            return False
                        c = complex(v)
                        return abs(c.imag) <= 1e-5
                    except Exception:
                        return False
                        
            h2_ok = is_conv(I2)
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        free_symbols = witness.free_symbols
        if len(free_symbols) == 0:
            try:
                c = complex(witness)
                # If constant is non-zero, integrals diverge, so conclusion fails
                neg_q_ok = (abs(c.real) > 1e-9)
            except Exception:
                neg_q_ok = False
        elif len(free_symbols) == 1:
            sym = list(free_symbols)[0]
            f = witness
            I1 = integrate(f, (sym, 0, oo))
            I2 = integrate(f**2, (sym, 0, oo))
            I3 = integrate(sym**2 * f**2, (sym, 0, oo))
            
            def get_val(I):
                if I.has(oo, zoo, nan, -oo):
                    return None
                try:
                    c = complex(I)
                    if abs(c.imag) > 1e-5:
                        return None
                    return c.real
                except Exception:
                    try:
                        v = I.evalf()
                        if v.has(oo, zoo, nan, -oo):
                            return None
                        c = complex(v)
                        if abs(c.imag) > 1e-5:
                            return None
                        return c.real
                    except Exception:
                        return None

            v1 = get_val(I1)
            v2 = get_val(I2)
            v3 = get_val(I3)

            # The conclusion fails if any integral diverges, or if the inequality is violated
            if v1 is None or v2 is None or v3 is None:
                neg_q_ok = True
            else:
                LHS = v1**4
                RHS = (math.pi**2) * v2 * v3
                if LHS > RHS + 1e-7:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a continuous, non-negative function on [0, \\infty)",
    "H_2: The improper integral \\int_0^\\infty f(x)^2 dx converges",
    "¬Q: The conclusion fails (inequality is violated or integrals diverge)"
]

N_HYP = 2
NEG_Q_INDEX = 2