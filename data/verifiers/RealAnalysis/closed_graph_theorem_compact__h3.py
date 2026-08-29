import sympy
from sympy import Symbol, Set, Interval, FiniteSet, Union, Limit, S
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the Closed Graph Theorem for Compact Spaces.
    
    Expected witness format:
      A dictionary {'X': Set, 'Y': Set, 'f': Expr, 'var': Symbol}
      or a tuple (X, Y, f) or (X, Y, f, var)
      or just a SymPy expression f (where X and Y default to Reals).
    """
    try:
        # 1. Parse witness
        if isinstance(witness, dict):
            X = witness.get('X', S.Reals)
            Y = witness.get('Y', S.Reals)
            f = witness.get('f', None)
            var = witness.get('var', None)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                X, Y, f = witness
                var = None
            elif len(witness) == 4:
                X, Y, f, var = witness
            else:
                return [False, False, False, False]
        elif isinstance(witness, sympy.Expr):
            X = S.Reals
            Y = S.Reals
            f = witness
            var = None
        else:
            return [False, False, False, False]

        if f is None:
            return [False, False, False, False]

        if isinstance(f, str):
            try:
                f = sympy.sympify(f)
            except Exception:
                return [False, False, False, False]

        if isinstance(f, sympy.Lambda):
            if var is None and len(f.variables) == 1:
                var = f.variables[0]
            f = f.expr

        if var is None:
            free = f.free_symbols
            if len(free) == 1:
                var = list(free)[0]
            else:
                var = Symbol('x')

        # H1: X is a topological space
        # In this context, any valid SymPy Set represents a topological space (subspace of R)
        try:
            h1 = isinstance(X, Set)
        except Exception:
            h1 = False

        # H2: Y is a compact metric space
        # A subset of R is compact iff it is closed and bounded.
        def is_compact(s):
            if s == S.EmptySet:
                return True
            if isinstance(s, FiniteSet):
                return True
            if isinstance(s, Interval):
                return not s.left_open and not s.right_open and s.start.is_finite and s.end.is_finite
            if isinstance(s, Union):
                return all(is_compact(arg) for arg in s.args)
            return False

        try:
            h2 = is_compact(Y)
        except Exception:
            h2 = False

        # H3: The graph G is a closed subset of X x Y
        # neg_Q: The function f is not continuous
        h3 = True
        is_continuous_on_X = True

        try:
            rng = function_range(f, var, X)
            if rng.is_subset(Y) == False:
                h3 = False
        except Exception:
            pass

        try:
            cont_dom = continuous_domain(f, var, X)
            discontinuities = X - cont_dom
            
            if not discontinuities.is_empty:
                if isinstance(discontinuities, FiniteSet):
                    for x0 in discontinuities:
                        # Check left limit if x0 is a limit point from the left in X
                        check_left = True
                        try:
                            if X.intersect(Interval.open(-oo, x0)).is_empty:
                                check_left = False
                        except Exception:
                            pass
                            
                        if check_left:
                            try:
                                L_left = Limit(f, var, x0, dir='-').doit()
                                if L_left.has(sympy.AccumBounds):
                                    h3 = False
                                    is_continuous_on_X = False
                                else:
                                    try:
                                        f_val = f.subs(var, x0)
                                    except Exception:
                                        f_val = None
                                    if f_val is None or L_left != f_val:
                                        is_continuous_on_X = False
                                        if Y.contains(L_left) == True:
                                            h3 = False
                            except Exception:
                                is_continuous_on_X = False
                                
                        # Check right limit if x0 is a limit point from the right in X
                        check_right = True
                        try:
                            if X.intersect(Interval.open(x0, oo)).is_empty:
                                check_right = False
                        except Exception:
                            pass
                            
                        if check_right:
                            try:
                                L_right = Limit(f, var, x0, dir='+').doit()
                                if L_right.has(sympy.AccumBounds):
                                    h3 = False
                                    is_continuous_on_X = False
                                else:
                                    try:
                                        f_val = f.subs(var, x0)
                                    except Exception:
                                        f_val = None
                                    if f_val is None or L_right != f_val:
                                        is_continuous_on_X = False
                                        if Y.contains(L_right) == True:
                                            h3 = False
                            except Exception:
                                is_continuous_on_X = False
                else:
                    h3 = False
                    is_continuous_on_X = False
        except Exception:
            h3 = False
            is_continuous_on_X = False

        neg_q = not is_continuous_on_X

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: Y is a compact metric space",
    "H_3: The graph G is a closed subset of X x Y",
    "¬Q: The function f is not continuous"
]

N_HYP = 3
NEG_Q_INDEX = 3