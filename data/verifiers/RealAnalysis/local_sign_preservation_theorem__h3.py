import sympy
from sympy import Symbol, S, limit, Interval

# Top-level setup for witness expressions
x = Symbol('x', real=True)
R = S.Reals

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Local Sign Preservation Theorem.
    The witness is expected to be a tuple: (f_expr, D, c)
      - f_expr: a sympy expression in terms of x representing the function f
      - D: a sympy Set representing the domain
      - c: a real number representing the point c
    """
    if not isinstance(witness, tuple) or len(witness) != 3:
        return [False, False, False]
        
    f_expr, D, c = witness
    
    # H_1: f is defined on D and c in D
    try:
        if D.contains(c) != S.true:
            h1 = False
        else:
            val_c = f_expr.subs(x, c)
            h1 = (val_c.is_real is not False)
    except Exception:
        h1 = False
        
    # H_2: f is continuous at c in D
    try:
        val_c = f_expr.subs(x, c)
        if val_c.is_real is False:
            h2 = False
        else:
            h2 = True
            
            # Check right limit if c is a limit point from the right
            is_right_limit_point = False
            for k in range(1, 5):
                if D.intersect(Interval.open(c, c + 10**-k)) != S.EmptySet:
                    is_right_limit_point = True
                    break
            if is_right_limit_point:
                lim_right = limit(f_expr, x, c, dir='+')
                if lim_right != val_c:
                    h2 = False
                    
            # Check left limit if c is a limit point from the left
            is_left_limit_point = False
            for k in range(1, 5):
                if D.intersect(Interval.open(c - 10**-k, c)) != S.EmptySet:
                    is_left_limit_point = True
                    break
            if is_left_limit_point:
                lim_left = limit(f_expr, x, c, dir='-')
                if lim_left != val_c:
                    h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: For all delta > 0, there exists x in D intersect (c-delta, c+delta) 
    #     where f(x) does not have the same sign as f(c)
    try:
        val_c = f_expr.subs(x, c)
        if val_c.is_real is False:
            neg_q = False
        else:
            sign_c = sympy.sign(val_c)
            neg_q = True
            
            # Test a sequence of shrinking neighborhoods (delta = 10^-1 down to 10^-5)
            for k in range(1, 6):
                delta = sympy.Rational(1, 10**k)
                found_diff_sign = False
                
                # Generate test points within the (c-delta, c+delta) neighborhood
                test_pts = []
                for m in range(2, 15):
                    test_pts.append(c + delta/m)
                    test_pts.append(c - delta/m)
                    
                for pt in test_pts:
                    if D.contains(pt) == S.true:
                        val_pt = f_expr.subs(x, pt)
                        if sympy.sign(val_pt) != sign_c:
                            found_diff_sign = True
                            break
                            
                # If we couldn't find any point with a different sign in this neighborhood,
                # then there exists a delta where all points have the same sign as f(c).
                # Thus the conclusion holds, and the negated conclusion is False.
                if not found_diff_sign:
                    neg_q = False
                    break
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is defined on D and c in D",
    "H_2: f is continuous at c in D",
    "¬Q: For all delta > 0, there exists x in D intersect (c-delta, c+delta) where f(x) does not have the same sign as f(c)"
]

N_HYP = 2
NEG_Q_INDEX = 2