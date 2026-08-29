import sympy
from sympy import Symbol, Interval, Union, FiniteSet, S, limit, AccumBounds
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def get_intervals(A):
    if isinstance(A, Interval):
        return [A]
    elif isinstance(A, Union):
        ints = []
        for arg in A.args:
            if isinstance(arg, Interval):
                ints.append(arg)
            elif isinstance(arg, Union):
                ints.extend(get_intervals(arg))
        return ints
    return []

def is_valid_limit(L):
    try:
        if L is None: return False
        if L.has(AccumBounds): return False
        if L in [S.Infinity, S.NegativeInfinity, S.ComplexInfinity, S.NaN]: return False
        if L.is_real is False: return False
        if L.is_finite is False: return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    witness is expected to be a tuple: (X, A, f)
    where X and A are sympy Sets, and f is a sympy Expr in terms of x.
    """
    try:
        X, A, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: X is a compact metric space (closed and bounded subset of Reals)
    try:
        h1_ok = bool(X.is_subset(S.Reals) and X.is_closed and X.is_bounded)
    except Exception:
        h1_ok = False
        
    # H_2: f: A -> R is a continuous function
    try:
        if not A.is_subset(X):
            h2_ok = False
        else:
            D = continuous_domain(f, x, A)
            h2_ok = bool(D == A)
    except Exception:
        h2_ok = False
        
    # ¬Q: There does NOT exist a continuous extension F: X -> R of f
    try:
        if not A.is_subset(X):
            neg_q = False
        else:
            # The boundary points of A in X
            pts_set = (A.closure & X) - A
            
            if pts_set.is_empty:
                # A is closed in X, so it's compact. By Tietze Extension Theorem, 
                # a continuous extension always exists.
                neg_q = False
            else:
                if not isinstance(pts_set, FiniteSet):
                    # For simplicity, we only handle cases with finitely many boundary holes
                    neg_q = False
                else:
                    pts = list(pts_set)
                    can_extend_all = True
                    intervals = get_intervals(A)
                    
                    for p in pts:
                        approach_left = False
                        approach_right = False
                        
                        for I in intervals:
                            if p == I.end and I.right_open:
                                approach_left = True
                            if p == I.start and I.left_open:
                                approach_right = True
                                
                        lim_left = None
                        lim_right = None
                        extendable_at_p = True
                        
                        if approach_left:
                            lim_left = limit(f, x, p, dir='-')
                            if not is_valid_limit(lim_left):
                                extendable_at_p = False
                                
                        if approach_right:
                            lim_right = limit(f, x, p, dir='+')
                            if not is_valid_limit(lim_right):
                                extendable_at_p = False
                                
                        if approach_left and approach_right and extendable_at_p:
                            if lim_left != lim_right:
                                extendable_at_p = False
                                
                        if not extendable_at_p:
                            can_extend_all = False
                            break
                            
                    neg_q = not can_extend_all
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: f: A -> R is a continuous function",
    "¬Q: There does not exist a continuous extension F: X -> R of f"
]

N_HYP = 2
NEG_Q_INDEX = 2