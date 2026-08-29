import sympy
from sympy import Symbol, Interval
from sympy.calculus.singularities import is_decreasing

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys 'f', 'g', 'a', 'b' or a tuple (f, g, a, b).
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, g, a, b = witness
            
        f = sympy.sympify(f, locals={'x': x})
        g = sympy.sympify(g, locals={'x': x})
        a = sympy.sympify(a, locals={'x': x})
        b = sympy.sympify(b, locals={'x': x})

        # Ensure all 'x' symbols in the expressions match our real 'x'
        for sym in f.free_symbols | g.free_symbols | a.free_symbols | b.free_symbols:
            if sym.name == 'x' and sym != x:
                f = f.subs(sym, x)
                g = g.subs(sym, x)
                a = a.subs(sym, x)
                b = b.subs(sym, x)
                
    except Exception:
        return [False, False]

    # H_1: f is monotonically decreasing on [a,b]
    h1_ok = False
    try:
        a_f = float(a)
        b_f = float(b)
        if a_f < b_f:
            res = is_decreasing(f, Interval(a, b), x)
            if res is True:
                h1_ok = True
            elif res is False:
                h1_ok = False
            else:
                # Fallback: check derivative at 101 sample points
                df = sympy.diff(f, x)
                h1_ok = True
                for i in range(101):
                    pt = a_f + (b_f - a_f) * i / 100.0
                    if float(df.subs(x, pt)) > 1e-9:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # ¬Q: \int_a^b f(x)g(x) dx > f(a) \int_a^b g(x) dx
    neg_q_ok = False
    try:
        lhs = sympy.integrate(f * g, (x, a, b))
        rhs = f.subs(x, a) * sympy.integrate(g, (x, a, b))
        
        try:
            diff_val = float(lhs - rhs)
        except TypeError:
            diff_val = float((lhs - rhs).evalf())
            
        if diff_val > 1e-9:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is monotonically decreasing on the interval a to b",
    "¬Q: integral of f(x)g(x) from a to b > f(a) * integral of g(x) from a to b"
]

N_HYP = 1
NEG_Q_INDEX = 1