import sympy
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: f is continuous on the closed interval",
    "H_2: f is strictly monotonic on the closed interval",
    "not Q: f does not have exactly one root in the open interval"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (f, a, b) where:
      - f is a sympy expression in terms of x
      - a and b are real numbers with a < b
    """
    if not isinstance(witness, tuple) or len(witness) != 3:
        return [False, False, False]
    
    f_expr, a_val, b_val = witness
    
    try:
        f = sympy.sympify(f_expr)
        a = sympy.sympify(a_val)
        b = sympy.sympify(b_val)
        if not a.is_real or not b.is_real:
            return [False, False, False]
        if not bool(a < b):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: f is continuous on the closed interval
    try:
        domain = sympy.calculus.util.continuous_domain(f, x, sympy.S.Reals)
        h1 = bool(sympy.Interval(a, b).is_subset(domain))
    except Exception:
        h1 = False
        
    # H2: f is strictly monotonic on the closed interval
    h2 = False
    try:
        f_prime = sympy.diff(f, x)
        
        # Check if strictly increasing
        try:
            min_deriv = sympy.calculus.util.minimum(f_prime, x, sympy.Interval(a, b))
            if bool(min_deriv > 0):
                h2 = True
            elif bool(min_deriv >= 0):
                zeros = sympy.solveset(f_prime, x, domain=sympy.Interval(a, b))
                if zeros.is_empty or isinstance(zeros, sympy.FiniteSet):
                    h2 = True
        except Exception:
            pass
            
        if not h2:
            # Check if strictly decreasing
            try:
                max_deriv = sympy.calculus.util.maximum(f_prime, x, sympy.Interval(a, b))
                if bool(max_deriv < 0):
                    h2 = True
                elif bool(max_deriv <= 0):
                    zeros = sympy.solveset(f_prime, x, domain=sympy.Interval(a, b))
                    if zeros.is_empty or isinstance(zeros, sympy.FiniteSet):
                        h2 = True
            except Exception:
                pass
                
        if not h2:
            # Fallback to solveset
            try:
                non_pos = sympy.solveset(f_prime <= 0, x, domain=sympy.Interval(a, b))
                if non_pos.is_empty or isinstance(non_pos, sympy.FiniteSet):
                    h2 = True
                else:
                    non_neg = sympy.solveset(f_prime >= 0, x, domain=sympy.Interval(a, b))
                    if non_neg.is_empty or isinstance(non_neg, sympy.FiniteSet):
                        h2 = True
            except Exception:
                pass
    except Exception:
        pass
        
    # neg_Q: f does not have exactly one root in the open interval
    neg_q = False
    try:
        roots = sympy.solveset(f, x, domain=sympy.Interval.open(a, b))
        if roots.is_empty:
            neg_q = True
        elif isinstance(roots, sympy.FiniteSet):
            neg_q = (len(roots) != 1)
        elif isinstance(roots, (sympy.ConditionSet, sympy.Intersection, sympy.ImageSet)):
            # Cannot definitively determine the number of roots
            neg_q = False
        else:
            # If it's an interval or union of intervals, it has infinitely many roots
            neg_q = True
    except Exception:
        pass
        
    return [h1, h2, neg_q]