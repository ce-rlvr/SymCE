import sympy
import math
import itertools
import functools

# Top-level setup for witness expressions
x = sympy.Symbol('x', real=True)
y = sympy.Symbol('y', real=True)
z = sympy.Symbol('z', real=True)

def is_compact(subset):
    """Helper to check if a SymPy set is a compact subset of Reals."""
    if subset == sympy.S.EmptySet:
        return True
    if isinstance(subset, sympy.FiniteSet):
        return True
    if isinstance(subset, sympy.Interval):
        return (not subset.left_open) and (not subset.right_open) and subset.start.is_finite and subset.end.is_finite
    if subset == sympy.S.Reals:
        return False
    if subset in (sympy.S.Integers, sympy.S.Naturals, sympy.S.Naturals0):
        return False
    if isinstance(subset, sympy.Union):
        args_compact = [is_compact(arg) for arg in subset.args]
        if all(a is True for a in args_compact):
            return True
        if any(a is False for a in args_compact):
            return False
        return None
    return None

def conditions(witness):
    """
    witness is expected to be a dict with keys:
      'X': SymPy Set (the domain)
      'Y': SymPy Set (the codomain)
      'f': SymPy Lambda (the function)
      'K': SymPy Set (the compact subset of Y)
    """
    # H1: Y is a metric space (subset of Reals)
    try:
        Y = witness['Y']
        h1 = (Y.is_subset(sympy.S.Reals) == True) or (Y == sympy.S.Reals)
    except Exception:
        h1 = False

    # H2: f: X -> Y is a continuous function
    try:
        X = witness['X']
        Y = witness['Y']
        f = witness['f']
        var = f.variables[0]
        expr = f.expr
        
        h2 = True
        
        # Check continuity
        try:
            cd = None
            if hasattr(sympy, 'continuous_domain'):
                cd = sympy.continuous_domain(expr, var, sympy.S.Reals)
            elif hasattr(sympy, 'calculus') and hasattr(sympy.calculus, 'util') and hasattr(sympy.calculus.util, 'continuous_domain'):
                cd = sympy.calculus.util.continuous_domain(expr, var, sympy.S.Reals)
                
            if cd is not None and not X.is_subset(cd):
                h2 = False
        except Exception:
            pass # fallback if continuous_domain fails
            
        # Check if f maps X to Y by sampling points
        try:
            points_to_check = []
            def add_points_from_set(S_set):
                if isinstance(S_set, sympy.Interval):
                    if S_set.start.is_finite and not S_set.left_open: points_to_check.append(S_set.start)
                    if S_set.end.is_finite and not S_set.right_open: points_to_check.append(S_set.end)
                    if S_set.start.is_finite and S_set.end.is_finite:
                        points_to_check.append((S_set.start + S_set.end)/2)
                    else:
                        if S_set.start.is_finite: points_to_check.append(S_set.start + 1)
                        elif S_set.end.is_finite: points_to_check.append(S_set.end - 1)
                        else: points_to_check.append(sympy.S(0))
                elif isinstance(S_set, sympy.FiniteSet):
                    points_to_check.extend(list(S_set))
                elif isinstance(S_set, sympy.Union):
                    for arg in S_set.args:
                        add_points_from_set(arg)
                elif S_set == sympy.S.Reals:
                    points_to_check.extend([sympy.S(0), sympy.S(1), sympy.S(-1)])
            
            add_points_from_set(X)
            
            for p in points_to_check:
                if p.is_real:
                    val = expr.subs(var, p)
                    contains_val = Y.contains(val)
                    if contains_val == False or contains_val == sympy.S.false:
                        h2 = False
        except Exception:
            pass
    except Exception:
        h2 = False

    # H3: K is a compact subset of Y
    try:
        K = witness['K']
        Y = witness['Y']
        if K.is_subset(Y) == True or K == Y:
            comp = is_compact(K)
            h3 = (comp is True)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The preimage f^{-1}(K) is not a compact subset of X
    try:
        X = witness['X']
        f = witness['f']
        K = witness['K']
        var = f.variables[0]
        expr = f.expr
        
        if isinstance(K, sympy.FiniteSet):
            preimage = sympy.S.EmptySet
            for k in K:
                sol = sympy.solveset(expr - k, var, domain=X)
                preimage = sympy.Union(preimage, sol)
        else:
            # For reliability, we only support FiniteSet for K in the counterexample
            preimage = None
            
        if preimage is not None:
            comp = is_compact(preimage)
            neg_q = (comp is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Y is a metric space",
    "H_2: f: X -> Y is a continuous function",
    "H_3: K is a compact subset of Y",
    "¬Q: The preimage f^{-1}(K) is not a compact subset of X"
]

N_HYP = 3
NEG_Q_INDEX = 3