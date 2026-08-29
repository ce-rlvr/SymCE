import sympy
from sympy import S, Symbol, Lambda, FiniteSet, Interval, Union, Intersection
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def get_expr_var(f):
    """Helper to extract a SymPy expression and variable from the witness function."""
    if callable(f) and not isinstance(f, sympy.Lambda):
        var = sympy.Symbol('x', real=True)
        expr = sympy.sympify(f(var))
    elif isinstance(f, sympy.Lambda):
        var = f.variables[0]
        expr = sympy.sympify(f.expr)
    else:
        expr = sympy.sympify(f)
        free = expr.free_symbols
        var = list(free)[0] if free else sympy.Symbol('x', real=True)
    return expr, var

def conditions(witness) -> list[bool]:
    try:
        X = witness.get('X')
        Y = witness.get('Y')
        f = witness.get('f')
        K = witness.get('K')
    except Exception:
        return [False, False, False, False]

    # H1: (X, d_X) and (Y, d_Y) are metric spaces
    # We verify this by checking if they are valid subsets of Reals.
    try:
        h1 = isinstance(X, sympy.Set) and X.is_subset(S.Reals) and \
             isinstance(Y, sympy.Set) and Y.is_subset(S.Reals)
    except Exception:
        h1 = False

    # H2: f: X -> Y is a continuous function
    try:
        expr, var = get_expr_var(f)
        if expr.is_constant():
            h2 = True
        else:
            cd = continuous_domain(expr, var, S.Reals)
            h2 = X.is_subset(cd)
    except Exception:
        h2 = False

    # H3: f is a closed map
    # A map to a finite set is always closed. A constant map is also closed.
    try:
        h3 = False
        if isinstance(Y, FiniteSet):
            h3 = True
        else:
            expr, var = get_expr_var(f)
            if sympy.simplify(sympy.diff(expr, var)) == 0:
                h3 = True
    except Exception:
        h3 = False

    # neg_Q: K is compact in Y, but f^{-1}(K) is not compact in X
    try:
        def is_compact(S_set):
            if isinstance(S_set, FiniteSet):
                return True
            if isinstance(S_set, Interval):
                return not S_set.left_open and not S_set.right_open and S_set.start.is_finite and S_set.end.is_finite
            if isinstance(S_set, Union):
                return all(is_compact(arg) for arg in S_set.args)
            if isinstance(S_set, Intersection):
                return any(is_compact(arg) for arg in S_set.args)
            if S_set == S.EmptySet:
                return True
            
            try:
                if S_set.inf.is_infinite or S_set.sup.is_infinite:
                    return False
            except Exception:
                pass

            if S_set in (S.Reals, S.Integers, S.Naturals, S.Naturals0):
                return False
                
            # Fallback: assume compact to avoid false positives for neg_Q
            return True

        if not K.is_subset(Y):
            neg_q = False
        elif not is_compact(K):
            neg_q = False
        else:
            expr, var = get_expr_var(f)
            if isinstance(K, FiniteSet):
                pre = S.EmptySet
                for k in K:
                    sol = sympy.solveset(sympy.Eq(expr, k), var, domain=X)
                    pre = Union(pre, sol)
            elif isinstance(K, Interval):
                sol = sympy.solveset(sympy.And(expr >= K.start, expr <= K.end), var, domain=X)
                pre = sol
            else:
                pre = None
            
            if pre is None:
                neg_q = False
            else:
                neg_q = not is_compact(pre)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: f: X -> Y is a continuous function",
    "H_3: f is a closed map",
    "¬Q: There exists a compact subset K in Y such that f^{-1}(K) is not compact in X"
]
N_HYP = 3
NEG_Q_INDEX = 3