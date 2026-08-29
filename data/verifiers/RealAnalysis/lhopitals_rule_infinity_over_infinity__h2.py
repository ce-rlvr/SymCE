import sympy
from sympy import Symbol, Interval, limit, solveset, diff, oo, EmptySet

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys 'f', 'g', 'a', 'b', 'L' or a tuple (f, g, a, b, L).
    """
    try:
        if isinstance(witness, dict):
            f = sympy.sympify(witness['f'], locals={'x': x})
            g = sympy.sympify(witness['g'], locals={'x': x})
            a = sympy.sympify(witness['a'], locals={'x': x})
            b = sympy.sympify(witness['b'], locals={'x': x})
            L = sympy.sympify(witness['L'], locals={'x': x})
        else:
            f, g, a, b, L = [sympy.sympify(w, locals={'x': x}) for w in witness]
    except Exception:
        return [False, False, False, False]

    try:
        if a >= b:
            return [False, False, False, False]
        if not (L.is_real or L == oo or L == -oo):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: f, g differentiable on (a, b)
    try:
        df = diff(f, x)
        dg = diff(g, x)
        
        if a == -oo and b == oo:
            mid = 0
        elif a == -oo:
            mid = b - 1
        elif b == oo:
            mid = a + 1
        else:
            mid = (a + b) / 2
            
        is_real_vals = f.subs(x, mid).is_real and g.subs(x, mid).is_real
        
        try:
            from sympy.calculus.util import continuous_domain
            dom_df = continuous_domain(df, x, Interval.open(a, b))
            dom_dg = continuous_domain(dg, x, Interval.open(a, b))
            h1 = is_real_vals and (dom_df == Interval.open(a, b)) and (dom_dg == Interval.open(a, b))
        except Exception:
            # Fallback if continuous_domain fails or is not available
            h1 = is_real_vals and df.subs(x, mid).is_real and dg.subs(x, mid).is_real
    except Exception:
        h1 = False

    # H2: g'(x) != 0 on (a, b)
    try:
        zeros = solveset(dg, x, domain=Interval.open(a, b))
        h2 = (zeros == EmptySet)
    except Exception:
        h2 = False

    # H3: limit(f'/g', x, a+) == L
    try:
        if a in [oo, -oo]:
            lim_fg_prime = limit(df / dg, x, a)
        else:
            lim_fg_prime = limit(df / dg, x, a, dir='+')
            
        if lim_fg_prime.has(sympy.Limit):
            h3 = False
        else:
            h3 = (lim_fg_prime == L)
    except Exception:
        h3 = False

    # neg_Q: limit(f/g, x, a+) != L
    try:
        if a in [oo, -oo]:
            lim_fg = limit(f / g, x, a)
        else:
            lim_fg = limit(f / g, x, a, dir='+')
            
        if lim_fg.has(sympy.Limit):
            neg_q = False
        else:
            neg_q = (lim_fg != L)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f and g are differentiable on (a, b)",
    "H_2: g'(x) != 0 for all x in (a, b)",
    "H_3: limit of f'(x)/g'(x) as x -> a^+ is L",
    "¬Q: limit of f(x)/g(x) as x -> a^+ is not L"
]

N_HYP = 3
NEG_Q_INDEX = 3