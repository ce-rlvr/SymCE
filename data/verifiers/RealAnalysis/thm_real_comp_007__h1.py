import sympy
from sympy import S, Symbol
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (D, f) where D is a sympy Set and f is a callable or sympy Expr.
    If only D is provided, f defaults to the identity function.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            D, f = witness
        else:
            D = witness
            f = x
    except Exception:
        return [False, False, False, False]

    try:
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = f
    except Exception:
        f_expr = x

    # H_1: D is a closed set
    try:
        if D == S.EmptySet:
            h1 = True
        else:
            h1 = D.is_subset(S.Reals) and D.boundary.is_subset(D)
    except Exception:
        h1 = False

    # H_2: f: D -> D is a function
    try:
        if D == S.EmptySet:
            h2 = True
        else:
            dom = continuous_domain(f_expr, x, S.Reals)
            if not D.is_subset(dom):
                h2 = False
            else:
                rng = function_range(f_expr, x, D)
                h2 = rng.is_subset(D)
    except Exception:
        h2 = False

    # H_3: There exists L in [0, 1) such that |f(x) - f(y)| <= L|x - y|
    try:
        if D == S.EmptySet:
            h3 = True
        else:
            f_prime = sympy.diff(f_expr, x)
            rng_prime = function_range(f_prime, x, D)
            h3 = (rng_prime.sup < 1) and (rng_prime.inf > -1)
    except Exception:
        h3 = False

    # ¬Q: There does not exist a unique fixed point x^* in D
    try:
        if D == S.EmptySet:
            neg_q = True
        else:
            fixed_points = sympy.solveset(sympy.Eq(f_expr, x), x, domain=D)
            if fixed_points == S.EmptySet:
                neg_q = True
            elif isinstance(fixed_points, sympy.FiniteSet):
                neg_q = len(fixed_points) != 1
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: D is a closed set",
    "H_2: f: D -> D is a function",
    "H_3: There exists L in [0, 1) such that |f(x) - f(y)| <= L|x - y|",
    "¬Q: There does not exist a unique fixed point x^* in D"
]

N_HYP = 3
NEG_Q_INDEX = 3