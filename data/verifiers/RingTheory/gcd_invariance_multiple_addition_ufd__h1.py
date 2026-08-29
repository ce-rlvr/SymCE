import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: a, b, c are non-zero elements",
    "¬Q: The greatest common divisor of a and b+ac is not equal to the greatest common divisor of a and b, up to a unit"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False]
        
    # H_1: a, b, c are non-zero elements
    try:
        def is_zero(x):
            try:
                if hasattr(x, 'is_zero_matrix'):
                    return x.is_zero_matrix
            except Exception:
                pass
            try:
                if hasattr(x, 'is_zero') and x.is_zero is not None:
                    return x.is_zero
            except Exception:
                pass
            try:
                return bool(x == x * 0)
            except Exception:
                pass
            try:
                return bool(x == 0)
            except Exception:
                return False

        if is_zero(a) or is_zero(b) or is_zero(c):
            h1 = False
        else:
            # Check if they are in the same ring by performing ring operations
            _ = b + a * c
            _ = a + b + c
            h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: gcd(a, b+ac) is NOT equal to gcd(a, b) up to a unit
    try:
        # If the objects are explicitly non-commutative or matrices, 
        # the standard commutative GCD is not defined or fails, making the conclusion false.
        if isinstance(a, sp.MatrixBase) or isinstance(b, sp.MatrixBase):
            neg_q = True
        elif hasattr(a, 'is_commutative') and a.is_commutative is False:
            neg_q = True
        else:
            def get_gcd(x, y):
                if hasattr(x, 'gcd'):
                    return x.gcd(y)
                return sp.gcd(x, y)
                
            term = b + a * c
            g1 = get_gcd(a, term)
            g2 = get_gcd(a, b)
            
            if g1 is None or g2 is None:
                neg_q = True
            else:
                are_equal = False
                try:
                    if g1 == g2:
                        are_equal = True
                except Exception:
                    pass
                
                if not are_equal:
                    try:
                        if g1 == -g2:
                            are_equal = True
                    except Exception:
                        pass
                        
                if not are_equal and hasattr(g1, 'is_associate'):
                    try:
                        are_equal = g1.is_associate(g2)
                    except Exception:
                        pass
                        
                if not are_equal and hasattr(g1, 'equals_up_to_unit'):
                    try:
                        are_equal = g1.equals_up_to_unit(g2)
                    except Exception:
                        pass
                
                neg_q = not are_equal
                
    except Exception as e:
        # If an exception explicitly indicates that the GCD does not exist or is undefined,
        # then the conclusion fails. Otherwise, we assume it's an evaluation limitation.
        msg = str(e).lower()
        if "not exist" in msg or "undefined" in msg or "not supported" in msg:
            neg_q = True
        else:
            neg_q = False
            
    return [h1, neg_q]