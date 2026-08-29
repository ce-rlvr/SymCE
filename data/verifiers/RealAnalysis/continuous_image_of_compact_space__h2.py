import sympy
from sympy import S, Symbol, Set, imageset, Interval
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys 'X', 'Y', 'K' (sympy Sets) and 'f' (sympy Expr or callable).
    """
    try:
        X = witness['X']
        Y = witness['Y']
        K = witness['K']
        f = witness['f']
    except (KeyError, TypeError):
        return [False, False, False]
        
    if callable(f):
        try:
            f_expr = f(x)
        except Exception:
            f_expr = f
    else:
        f_expr = f

    # H_1: X and Y are metric spaces (and K is a subset of X)
    try:
        h1 = isinstance(X, Set) and isinstance(Y, Set) and isinstance(K, Set)
        if h1:
            h1 = (K.is_subset(X) == True)
    except Exception:
        h1 = False

    # H_2: f is a continuous function from X to Y
    try:
        dom = continuous_domain(f_expr, x, S.Reals)
        is_cont = (X.is_subset(dom) == True)
        
        img_X = imageset(x, f_expr, X)
        is_to_Y = (img_X.is_subset(Y) == True)
        
        h2 = is_cont and is_to_Y
    except Exception:
        h2 = False

    # neg_Q: f(K) is not compact
    # A subset of R is compact iff it is closed and bounded.
    try:
        img_K = imageset(x, f_expr, K)
        is_closed = img_K.is_closed
        is_bounded = img_K.is_bounded
        
        if is_closed == True and is_bounded == True:
            neg_q = False
        elif is_closed == False or is_bounded == False:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces (and K is a subset of X)",
    "H_2: f: X -> Y is a continuous function",
    "¬Q: The image f(K) is not a compact subset of Y"
]

N_HYP = 2
NEG_Q_INDEX = 2