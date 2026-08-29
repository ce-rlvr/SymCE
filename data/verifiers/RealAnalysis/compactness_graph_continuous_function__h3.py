import sympy
from sympy import Set, Symbol, Interval, Piecewise, Eq, S
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup for witness expressions
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            X = witness.get('X')
            Y = witness.get('Y')
            f = witness.get('f')
        elif isinstance(witness, tuple) and len(witness) == 3:
            X, Y, f = witness
        elif hasattr(witness, 'X') and hasattr(witness, 'Y') and hasattr(witness, 'f'):
            X = witness.X
            Y = witness.Y
            f = witness.f
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: X is a compact metric space
    # In R, a set is compact iff it is closed and bounded.
    try:
        h1 = bool(X.is_closed and X.is_bounded)
    except Exception:
        h1 = False

    # H2: Y is a metric space
    # Any subset of R (represented as a SymPy Set) is a metric space.
    try:
        h2 = isinstance(Y, Set)
    except Exception:
        h2 = False

    # ¬Q: The graph of f is NOT compact
    # Theorem: If X is compact and Y is Hausdorff (e.g. a metric space), 
    # the graph of f is compact if and only if f is continuous.
    # Therefore, the graph is NOT compact iff f is NOT continuous on X.
    try:
        if callable(f):
            try:
                f_expr = f(x)
            except Exception:
                f_expr = f
        else:
            f_expr = f
            
        if isinstance(f_expr, str):
            f_expr = sympy.sympify(f_expr)
            
        if hasattr(f_expr, 'free_symbols') and len(f_expr.free_symbols) > 0:
            if x in f_expr.free_symbols:
                x_sym = x
            else:
                x_sym = list(f_expr.free_symbols)[0]
        else:
            x_sym = x
            
        cont_dom = continuous_domain(f_expr, x_sym, X)
        
        if isinstance(cont_dom, sympy.ConditionSet):
            # Fallback if continuous_domain cannot fully evaluate
            frange = function_range(f_expr, x_sym, X)
            neg_q = not bool(frange.is_bounded)
        else:
            # If X is not a subset of the continuous domain, f is discontinuous on X
            neg_q = not bool(X.is_subset(cont_dom))
            
            # Double check for unboundedness if SymPy claims it is continuous
            if not neg_q:
                try:
                    frange = function_range(f_expr, x_sym, X)
                    if not bool(frange.is_bounded):
                        neg_q = True
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: Y is a metric space",
    "¬Q: The graph of f is not compact"
]

N_HYP = 2
NEG_Q_INDEX = 2