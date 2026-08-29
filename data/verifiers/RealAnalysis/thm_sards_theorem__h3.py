import sympy
from sympy import Matrix, eye, zeros, solve, S, Abs, sign, Piecewise
import itertools
from sympy.abc import x, y, z, t, u, v, w

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    """
    # H_1: U is an open subset of R^n
    try:
        U = witness.get('U', None)
        h1 = True
        if U is not None and hasattr(U, 'is_open'):
            if U.is_open is False:
                h1 = False
    except Exception:
        h1 = False

    # H_2: f is a smooth (C^\infty) function
    try:
        f = witness['f']
        vars_ = witness['vars']
        if not isinstance(vars_, (list, tuple)):
            vars_ = [vars_]
            
        if callable(f):
            f = f(*vars_)
            
        if isinstance(f, (list, tuple)):
            f = Matrix(f)
        elif not isinstance(f, Matrix):
            f = Matrix([f])
            
        h2 = True
        for i in range(f.shape[0]):
            expr = f[i]
            # Check for obvious non-smooth components
            if expr.has(Abs) or expr.has(sign) or expr.has(Piecewise):
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The set of critical values f(C) does NOT have Lebesgue measure zero in R^m
    try:
        n = witness['n']
        m = witness['m']
        f = witness['f']
        vars_ = witness['vars']
        
        if not isinstance(vars_, (list, tuple)):
            vars_ = [vars_]
            
        if callable(f):
            f = f(*vars_)
            
        if isinstance(f, (list, tuple)):
            f = Matrix(f)
        elif not isinstance(f, Matrix):
            f = Matrix([f])
            
        J = f.jacobian(vars_)
        
        neg_q = False
        if n < m:
            # The image of R^n in R^m has Hausdorff dimension <= n < m, so its m-dimensional measure is 0.
            neg_q = False
        elif m == 1:
            eqs = [J[0, i] for i in range(n)]
            sols = solve(eqs, vars_, dict=True)
            if isinstance(sols, list):
                for sol in sols:
                    val = f[0].subs(sol)
                    # If the critical value is not constant and depends on free variables,
                    # it may cover an interval, meaning positive measure.
                    if not val.is_constant() and val.free_symbols:
                        neg_q = True
                        break
        else:
            minors = []
            for cols in itertools.combinations(range(n), m):
                sub_J = J[:, cols]
                minors.append(sub_J.det())
            sols = solve(minors, vars_, dict=True)
            if isinstance(sols, list):
                for sol in sols:
                    val = f.subs(sol)
                    is_const = all(v.is_constant() for v in val)
                    has_free = any(v.free_symbols for v in val)
                    if not is_const and has_free:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: f is a smooth (C^infty) function",
    "¬Q: The set of critical values f(C) does not have Lebesgue measure zero in R^m"
]

N_HYP = 2
NEG_Q_INDEX = 2