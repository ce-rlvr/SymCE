import sympy
from sympy.calculus.util import continuous_domain

# Top-level setup for witness expressions
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should provide the space X, function f, points a and b, and value y.
    """
    try:
        if isinstance(witness, dict):
            X = witness.get('X')
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
            y = witness.get('y')
        else:
            X, f, a, b, y = witness
    except Exception:
        return [False, False, False, False]

    # If f is provided as a lambda/callable, convert it to a sympy expression
    if callable(f):
        try:
            f = f(x)
        except Exception:
            pass

    # H_1: X is a connected topological space
    # In the real line, connected sets are intervals, the whole real line, or singletons.
    try:
        h1 = isinstance(X, sympy.Interval) or X == sympy.S.Reals or (isinstance(X, sympy.FiniteSet) and len(X) == 1)
    except Exception:
        h1 = False

    # H_2: f: X -> R is a continuous function
    try:
        dom = continuous_domain(f, x, X)
        h2 = (dom == X)
    except Exception:
        h2 = False

    # H_3: a and b are points in X
    try:
        h3 = (sympy.sympify(X.contains(a)) == sympy.S.true) and (sympy.sympify(X.contains(b)) == sympy.S.true)
    except Exception:
        h3 = False

    # ¬Q: There does NOT exist a point c in X such that f(c) = y
    try:
        sol = sympy.solveset(f - y, x, domain=X)
        if isinstance(sol, sympy.ConditionSet):
            neg_q = False
        else:
            neg_q = (sol == sympy.S.EmptySet)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a connected topological space",
    "H_2: f: X -> R is a continuous function",
    "H_3: a and b are points in X",
    "¬Q: There is no point c in X such that f(c) = y"
]

N_HYP = 3
NEG_Q_INDEX = 3