import sympy
from sympy import Symbol, S, Interval, FiniteSet, Union, ImageSet
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup: named object bindings
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Evaluates the conditions for the conjecture.
    Expected witness: a tuple (X, f) or (X, f, Y)
    where X is a SymPy Set and f is a SymPy Expr in terms of x.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                X, f = witness
            elif len(witness) >= 3:
                X, f = witness[0], witness[1]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: f: X \to Y is a continuous map
    try:
        dom = continuous_domain(f, x, S.Reals)
        h1 = bool(X.is_subset(dom))
    except Exception:
        h1 = False

    def is_path_connected(S_set):
        if S_set == S.Reals or S_set == S.EmptySet:
            return True
        if isinstance(S_set, Interval):
            return True
        if isinstance(S_set, FiniteSet):
            return len(S_set) <= 1
        if isinstance(S_set, Union):
            # SymPy automatically simplifies overlapping intervals.
            # If it remains a Union, it consists of disjoint sets.
            return False
        return None

    # H_2: X is a path-connected space
    try:
        q2 = is_path_connected(X)
        h2 = False if q2 is None else q2
    except Exception:
        h2 = False

    # ¬Q: The image f(X) is not a path-connected subspace of Y
    try:
        f_X = function_range(f, x, X)
        q = is_path_connected(f_X)
        if q is None:
            # Fallback to imageset if function_range returns an unevaluated object
            f_X2 = sympy.imageset(x, f, X)
            q2 = is_path_connected(f_X2)
            if q2 is None:
                neg_q = False
            else:
                neg_q = not q2
        else:
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f: X \\to Y is a continuous map",
    "H_2: X is a path-connected space",
    "¬Q: The image f(X) is not a path-connected subspace of Y"
]

N_HYP = 2
NEG_Q_INDEX = 2