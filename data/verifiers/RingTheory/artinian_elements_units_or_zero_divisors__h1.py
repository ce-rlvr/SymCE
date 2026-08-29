import math
import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains import Domain

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is an Artinian ring",
    "H_3: x is an element of R",
    "¬Q: x is neither a unit nor a zero divisor"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # Extract R and x from the witness
        if isinstance(witness, dict):
            R = witness.get('R')
            x = witness.get('x')
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        else:
            R = getattr(witness, 'R', None)
            x = getattr(witness, 'x', None)
            
        if R is None or x is None:
            return [False, False, False, False]
            
        # Handle the common case where R is represented by an integer n (for Z/nZ)
        if isinstance(R, int) or (hasattr(R, 'is_Integer') and R.is_Integer):
            try:
                R_val = int(R)
                if R_val <= 1:
                    return [False, False, False, False]
                h1 = True
                h2 = True  # Finite rings are Artinian
                try:
                    x_val = int(x)
                    h3 = 0 <= x_val < R_val
                    is_u = math.gcd(x_val, R_val) == 1
                    is_zd = (x_val != 0) and (math.gcd(x_val, R_val) > 1)
                    neg_q = not (is_u or is_zd)
                except Exception:
                    h3 = False
                    neg_q = False
                return [h1, h2, h3, neg_q]
            except Exception:
                pass
                
        # H1: R has a multiplicative identity
        def check_h1():
            if hasattr(R, 'has_multiplicative_identity'):
                if callable(R.has_multiplicative_identity):
                    return R.has_multiplicative_identity()
                return R.has_multiplicative_identity
            if hasattr(R, 'one') or hasattr(R, 'identity'):
                return True
            if isinstance(R, Domain):
                return True
            return False
            
        h1 = bool(check_h1())
        
        # H2: R is an Artinian ring
        def check_h2():
            if hasattr(R, 'is_artinian'):
                if callable(R.is_artinian):
                    return R.is_artinian()
                return R.is_artinian
            if isinstance(R, Domain):
                if R.is_Field:
                    return True
                if R == ZZ:
                    return False
                if hasattr(R, 'is_Poly') and R.is_Poly:
                    return False
            if hasattr(R, 'is_finite') and R.is_finite:
                return True
            return False
            
        h2 = bool(check_h2())
        
        # H3: x is an element of R
        def check_h3():
            if hasattr(R, '__contains__'):
                try:
                    if x in R:
                        return True
                except Exception:
                    pass
            if isinstance(R, Domain):
                try:
                    return x in R
                except Exception:
                    pass
            if hasattr(R, 'contains'):
                if callable(R.contains):
                    return R.contains(x)
            return False
            
        h3 = bool(check_h3())
        
        # Conclusion: x is either a unit or a zero divisor
        def check_unit():
            if hasattr(R, 'is_unit'):
                if callable(R.is_unit):
                    return R.is_unit(x)
                return R.is_unit
            if isinstance(R, Domain):
                if R.is_Field:
                    return x != R.zero
                if R == ZZ:
                    return x in [1, -1]
            if hasattr(R, 'is_Field') and R.is_Field:
                return x != 0
            return False
            
        def check_zero_divisor():
            if hasattr(R, 'is_zero_divisor'):
                if callable(R.is_zero_divisor):
                    return R.is_zero_divisor(x)
                return R.is_zero_divisor
            if isinstance(R, Domain):
                if x == R.zero:
                    return False
                if R.is_Field:
                    return False
                if R == ZZ:
                    return False
            if hasattr(R, 'is_Field') and R.is_Field:
                return False
            return False
            
        is_u = bool(check_unit())
        is_zd = bool(check_zero_divisor())
        
        neg_q = not (is_u or is_zd)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]