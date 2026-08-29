import sympy
from sympy import Symbol, S, oo, solveset, Abs, limit
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the entire real line R",
    "H_2: f is continuous everywhere on R",
    "H_3: The limit of |f(x)| as |x| approaches infinity is infinity",
    "¬Q: The set {x in R | f(x) = c} is unbounded"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_unbounded(s):
    try:
        if s.is_empty:
            return False
        if s.is_FiniteSet:
            return False
        if isinstance(s, sympy.Interval):
            return s.start == -sympy.oo or s.end == sympy.oo
        if isinstance(s, sympy.Union):
            return any(is_unbounded(arg) for arg in s.args)
        if isinstance(s, sympy.Complement):
            return is_unbounded(s.args[0])
        if isinstance(s, sympy.ImageSet):
            return True
        if hasattr(s, 'sup') and hasattr(s, 'inf'):
            if s.sup == sympy.oo or s.inf == -sympy.oo:
                return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # Parse witness
    f = None
    c = 0
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 2:
                f, c = witness[0], witness[1]
            elif len(witness) == 1:
                f = witness[0]
        elif isinstance(witness, dict):
            f = witness.get('f', witness.get('expression', None))
            c = witness.get('c', 0)
        else:
            f = witness
            
        if callable(f) and not isinstance(f, sympy.Basic):
            f = f(x)
            
        if not isinstance(f, sympy.Basic):
            f = sympy.sympify(f)
            
        if isinstance(c, sympy.Basic) and c.free_symbols:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    # H1 & H2: defined and continuous on R
    try:
        dom = continuous_domain(f, x, S.Reals)
        h1_ok = (dom == S.Reals)
        h2_ok = h1_ok
        if f.has(sympy.I):
            h1_ok = False
            h2_ok = False
    except Exception:
        h1_ok = False
        h2_ok = False

    # H3: limit of |f(x)| as |x| -> oo is oo
    try:
        lim_pos = limit(Abs(f), x, oo)
        lim_neg = limit(Abs(f), x, -oo)
        h3_ok = (lim_pos == oo) and (lim_neg == oo)
    except Exception:
        h3_ok = False

    # neg_Q: {x in R | f(x) = c} is unbounded
    try:
        level_set = solveset(f - c, x, domain=S.Reals)
        neg_q_ok = is_unbounded(level_set)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]