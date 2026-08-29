import sympy
import math

# Top-level setup
# (No specific named objects are required for this conjecture)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    
    def check_H1():
        try:
            if not isinstance(witness, sympy.Expr):
                w = sympy.sympify(witness)
            else:
                w = witness
            if hasattr(w, "free_symbols") and len(w.free_symbols) > 0:
                return False
            # Must be evaluable to a complex number
            c = complex(w.evalf())
            # Exclude infinities
            if w == sympy.zoo or w == sympy.oo or w == -sympy.oo:
                return False
            return True
        except Exception:
            return False

    def check_neg_Q():
        try:
            if not isinstance(witness, sympy.Expr):
                w = sympy.sympify(witness)
            else:
                w = witness
                
            tan_val = sympy.tan(w)
            
            # If tan(x) is undefined or infinite, it cannot be equal to a complex number
            if tan_val == sympy.zoo or tan_val == sympy.nan or tan_val == sympy.oo or tan_val == -sympy.oo:
                return True
                
            tan_num = complex(tan_val.evalf())
            
            x_num = complex(sympy.N(w))
            A_prev, A_curr = 0j, x_num
            B_prev, B_curr = 1j, 1j + 0j
            
            for n in range(2, 1000):
                A_next = (2 * n - 1) * A_curr - x_num**2 * A_prev
                B_next = (2 * n - 1) * B_curr - x_num**2 * B_prev
                
                max_val = max(abs(A_next), abs(B_next))
                if max_val > 1e150:
                    A_next /= 1e150
                    B_next /= 1e150
                    A_curr /= 1e150
                    B_curr /= 1e150
                    
                A_prev, A_curr = A_curr, A_next
                B_prev, B_curr = B_curr, B_next
                
            if abs(B_curr) < 1e-15:
                return True
                
            cf_val = A_curr / B_curr
            
            if abs(tan_num - cf_val) > 1e-5 * max(1.0, abs(tan_num)):
                return True
            else:
                return False
        except Exception:
            return True

    return [check_H1(), check_neg_Q()]

CONDITION_LABELS = [
    "H_1: x is a complex number",
    "¬Q: tan(x) is not equal to the generalized continued fraction"
]

N_HYP = 1
NEG_Q_INDEX = 1