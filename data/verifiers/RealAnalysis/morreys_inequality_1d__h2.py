import sympy
from sympy import Symbol, Piecewise, Abs, oo
import math
import itertools
import functools

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, p) where f is a sympy expression in x or a callable,
    and p is a real number.
    """
    try:
        f, p = witness
    except Exception:
        return [False, False]
        
    # H_1: p > 1 is a real number
    try:
        h1 = float(p) > 1.0
    except Exception:
        h1 = False
        
    # neg_Q: f does not admit a continuous representative or the inequality fails
    neg_q = False
    try:
        if isinstance(f, sympy.Expr):
            # Try to compute the derivative
            df = sympy.diff(f, x)
            
            is_df_zero = False
            try:
                if df.equals(0):
                    is_df_zero = True
            except Exception:
                pass
                
            # Fallback numerical check for zero derivative
            if not is_df_zero:
                test_pts = [-3.14159, -1.0, -0.5, 0.1234, 1.0, 2.71828, 10.0]
                all_zero = True
                for pt in test_pts:
                    try:
                        val = float(df.subs(x, pt))
                        if abs(val) > 1e-7:
                            all_zero = False
                            break
                    except Exception:
                        pass
                if all_zero:
                    is_df_zero = True
                    
            # If derivative is zero almost everywhere, check if f is constant
            if is_df_zero:
                test_pts = [-3.14159, -1.0, -0.5, 0.1234, 1.0, 2.71828, 10.0]
                vals = []
                for pt in test_pts:
                    try:
                        vals.append(float(f.subs(x, pt)))
                    except Exception:
                        pass
                if len(vals) > 0 and max(vals) - min(vals) > 1e-7:
                    # f is not constant but f' = 0 a.e., so LHS > 0 and RHS = 0
                    neg_q = True
                    
            # Check for essential discontinuities (meaning no continuous representative exists)
            if not neg_q:
                jump_points = [0.0, -1.0, 1.0, 0.5, -0.5]
                try:
                    for atom in f.atoms(sympy.Number):
                        try:
                            jump_points.append(float(atom))
                        except Exception:
                            pass
                except Exception:
                    pass
                
                for pt in set(jump_points):
                    try:
                        left = float(f.limit(x, pt, '-'))
                        right = float(f.limit(x, pt, '+'))
                        if abs(left - right) > 1e-7:
                            neg_q = True
                            break
                    except Exception:
                        # Fallback to numerical check if limit fails
                        try:
                            val_left = float(f.subs(x, pt - 1e-7))
                            val_right = float(f.subs(x, pt + 1e-7))
                            if abs(val_left - val_right) > 1e-3:
                                neg_q = True
                                break
                        except Exception:
                            pass
        else:
            # Witness is a callable (Python function)
            test_pts = [-3.14159, -1.0, -0.5, 0.1234, 1.0, 2.71828, 10.0]
            is_df_zero = True
            for pt in test_pts:
                try:
                    val1 = float(f(pt))
                    val2 = float(f(pt + 1e-5))
                    df_val = (val2 - val1) / 1e-5
                    if abs(df_val) > 1e-3:
                        is_df_zero = False
                        break
                except Exception:
                    pass
                    
            if is_df_zero:
                vals = []
                for pt in test_pts:
                    try:
                        vals.append(float(f(pt)))
                    except Exception:
                        pass
                if len(vals) > 0 and max(vals) - min(vals) > 1e-7:
                    neg_q = True
                    
            if not neg_q:
                for pt in [0, -1, 1, 0.5, -0.5, 2, -2, 3, -3, 5, -5, 10, -10]:
                    try:
                        val_left = float(f(pt - 1e-7))
                        val_right = float(f(pt + 1e-7))
                        if abs(val_left - val_right) > 1e-3:
                            neg_q = True
                            break
                    except Exception:
                        pass
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p > 1 is a real number",
    "¬Q: f does not admit a continuous representative or the inequality fails"
]

N_HYP = 1
NEG_Q_INDEX = 1