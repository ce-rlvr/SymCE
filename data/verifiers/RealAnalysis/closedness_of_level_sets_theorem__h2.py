import sympy
from sympy import Symbol, Interval, solveset, Eq, S, Piecewise

# Top-level setup
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on a closed interval",
    "H_2: c is a real number",
    "¬Q: The set of points where f equals c is not closed"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_not_closed_set(s):
    try:
        closure = s.closure
        if type(closure).__name__ != 'Closure':
            return closure != s
    except Exception:
        pass
    
    if isinstance(s, sympy.Interval):
        return s.left_open or s.right_open
    if isinstance(s, sympy.Union):
        return any(is_not_closed_set(arg) for arg in s.args)
    if isinstance(s, sympy.Intersection):
        return any(is_not_closed_set(arg) for arg in s.args)
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False]
        f, a, b, c = witness
        f = sympy.sympify(f)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        c = sympy.sympify(c)
    except Exception:
        return [False, False, False]

    # H_1: f is a real-valued function defined on the closed interval
    h1_ok = False
    try:
        a_val = float(a)
        b_val = float(b)
        if a_val < b_val and isinstance(f, sympy.Expr):
            free_syms = f.free_symbols
            if free_syms.issubset({x}):
                h1_ok = True
                
                # Check for obvious singularities (poles) in the interval
                try:
                    sings = sympy.singularities(f, x)
                    if sings.intersect(sympy.Interval(a, b)) != sympy.S.EmptySet:
                        h1_ok = False
                except Exception:
                    pass
    except Exception:
        h1_ok = False

    # H_2: c is a real number
    h2_ok = False
    try:
        c_val = float(c)
        h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The set is not closed
    neg_q_ok = False
    try:
        domain = sympy.Interval(a, b)
        L = sympy.solveset(sympy.Eq(f, c), x, domain=domain)
        
        if isinstance(L, sympy.ConditionSet):
            neg_q_ok = False
        else:
            neg_q_ok = is_not_closed_set(L)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]