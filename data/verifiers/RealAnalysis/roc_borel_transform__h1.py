import sympy
import math

# Top-level setup
n = sympy.Symbol('n', integer=True, nonnegative=True)

def conditions(witness):
    """
    Checks if the witness sequence a_n provides a counterexample.
    The conclusion is that the radius of convergence of sum a_n/n! x^n is infinity.
    We return neg_Q = True if the radius of convergence is NOT infinity.
    """
    try:
        if callable(witness):
            a_n = witness(n)
        else:
            a_n = witness
            
        c_n = a_n / sympy.factorial(n)
        
        # If the sequence is identically zero, the radius of convergence is infinity.
        if c_n == 0:
            return [False]
            
        # Try the ratio test analytically
        try:
            c_n_plus_1 = c_n.subs(n, n + 1)
            ratio = sympy.Abs(c_n / c_n_plus_1)
            L_ratio = sympy.limit(ratio, n, sympy.oo)
            if not isinstance(L_ratio, sympy.Limit):
                neg_q = (L_ratio != sympy.oo)
                return [bool(neg_q)]
        except Exception:
            pass
            
        # Try the root test analytically
        try:
            root = sympy.Abs(c_n)**(1/n)
            L_root = sympy.limit(root, n, sympy.oo)
            if not isinstance(L_root, sympy.Limit):
                neg_q = (L_root != 0)
                return [bool(neg_q)]
        except Exception:
            pass
            
        # Fallback: evaluate the root test numerically for large n.
        # If the radius of convergence is infinity, |c_n|^(1/n) must converge to 0.
        # We check if the sequence of roots is decreasing towards 0.
        v_max_200 = max(float(sympy.Abs(c_n.subs(n, i))**(1.0/i)) for i in range(200, 205))
        v_max_300 = max(float(sympy.Abs(c_n.subs(n, i))**(1.0/i)) for i in range(300, 305))
        
        if v_max_300 < 1e-5:
            neg_q = False
        else:
            # If it's going to 0 like C/n, the difference should be roughly v_max_300 / 2.
            # We use a threshold of v_max_300 / 4 to safely detect convergence to 0.
            is_going_to_zero = (v_max_200 - v_max_300) > (v_max_300 / 4.0)
            neg_q = not is_going_to_zero
            
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the series sum a_n/n! x^n is not infinity"
]

N_HYP = 0
NEG_Q_INDEX = 0