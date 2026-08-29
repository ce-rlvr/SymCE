import sympy
from sympy import S, Interval, Union, Intersection, FiniteSet, ProductSet
from sympy.abc import x, y, z

# Define symbols for sequences
m = sympy.Symbol('m', integer=True, positive=True)
n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Check if the witness is a valid counterexample.
    The witness should be a tuple (K, seq) where:
      - K is a sympy Set representing a subset of R^n.
      - seq is a sympy expression (or list/tuple of expressions for R^n) in terms of m,
        or a callable that takes m and returns such an expression.
    """
    try:
        K, seq = witness
    except Exception:
        return [False, False]
    
    # H_1: K is a compact subset of R^n
    try:
        h1 = False
        def is_compact_R1(S_1):
            if S_1 == S.EmptySet:
                return True
            if S_1.is_subset(S.Reals) == True:
                if getattr(S_1, 'is_closed', False) == True:
                    inf = getattr(S_1, 'inf', None)
                    sup = getattr(S_1, 'sup', None)
                    if inf is not None and sup is not None:
                        if getattr(inf, 'is_finite', False) == True and getattr(sup, 'is_finite', False) == True:
                            return True
            return False

        if is_compact_R1(K):
            h1 = True
        elif isinstance(K, ProductSet):
            if all(is_compact_R1(arg) for arg in K.args):
                h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: The sequence (x_m) does not converge to a limit L that belongs to K
    try:
        if callable(seq):
            seq_expr = seq(m)
        else:
            seq_expr = seq
            
        if isinstance(seq_expr, (list, tuple, sympy.Tuple)):
            comps = seq_expr
        elif hasattr(seq_expr, 'is_Matrix') and seq_expr.is_Matrix:
            comps = list(seq_expr)
        else:
            comps = None
            
        if comps is not None:
            limits = [sympy.limit(comp, m, sympy.oo) for comp in comps]
            if all(hasattr(l, 'is_number') and l.is_number and getattr(l, 'is_finite', False) == True for l in limits):
                L = sympy.Tuple(*limits)
                in_K = sympy.simplify(K.contains(L))
                if in_K == sympy.S.true or in_K == True:
                    neg_q = False
                else:
                    neg_q = True
            else:
                neg_q = True
        else:
            L = sympy.limit(seq_expr, m, sympy.oo)
            if hasattr(L, 'is_number') and L.is_number and getattr(L, 'is_finite', False) == True:
                in_K = sympy.simplify(K.contains(L))
                if in_K == sympy.S.true or in_K == True:
                    neg_q = False
                else:
                    neg_q = True
            else:
                neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a compact subset of R^n",
    "¬Q: The sequence (x_m) does not converge to a limit L that belongs to K"
]

N_HYP = 1
NEG_Q_INDEX = 1