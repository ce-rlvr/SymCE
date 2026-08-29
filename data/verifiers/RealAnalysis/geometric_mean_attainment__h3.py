import sympy
from sympy import Symbol, Interval
from sympy.calculus.util import continuous_domain, minimum, maximum

x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        f, a, b = witness
        f = sympy.sympify(f)
    except Exception:
        return [False, False, False]
        
    # H1: f is a real-valued function defined on the interval
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        if not (a_sym.is_real and b_sym.is_real and bool(a_sym < b_sym)):
            h1 = False
        else:
            fa = complex(f.subs(x, a_sym).evalf())
            fb = complex(f.subs(x, b_sym).evalf())
            if abs(fa.imag) > 1e-9 or abs(fb.imag) > 1e-9:
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # H2: f is continuous on the interval
    try:
        domain = continuous_domain(f, x, Interval(a_sym, b_sym))
        h2 = (domain == Interval(a_sym, b_sym))
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist c such that f(c) = sqrt(f(a)*f(b))
    try:
        fa_val = complex(f.subs(x, a_sym).evalf())
        fb_val = complex(f.subs(x, b_sym).evalf())
        V_val = fa_val * fb_val
        
        if abs(V_val.imag) > 1e-7:
            neg_q = False
        elif V_val.real < -1e-7:
            # V is negative, so sqrt(V) is imaginary. Since f is real-valued, it never attains an imaginary value.
            neg_q = True
        else:
            target_val = V_val.real ** 0.5
            try:
                min_val = minimum(f, x, Interval(a_sym, b_sym))
                max_val = maximum(f, x, Interval(a_sym, b_sym))
                min_f = float(min_val.evalf())
                max_f = float(max_val.evalf())
            except Exception:
                # Fallback to grid search if exact minimum/maximum fails
                min_f = float('inf')
                max_f = float('-inf')
                N = 1000
                a_f = float(a_sym)
                b_f = float(b_sym)
                for i in range(N + 1):
                    val = a_f + i * (b_f - a_f) / N
                    try:
                        fv = float(f.subs(x, val).evalf())
                        if fv < min_f: min_f = fv
                        if fv > max_f: max_f = fv
                    except Exception:
                        pass
            
            # If target is strictly outside the range of f on the interval, it is never attained.
            if target_val < min_f - 1e-7 or target_val > max_f + 1e-7:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the closed interval",
    "H_2: f is continuous on the closed interval",
    "¬Q: There does not exist c such that f(c) = sqrt(f(a)f(b))"
]

N_HYP = 2
NEG_Q_INDEX = 2