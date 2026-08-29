import sympy
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: The ideal quotient (a) : (b) is not equal to the principal ideal (a / gcd(a, b))"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
                R = sympy.ZZ
            elif len(witness) == 3:
                R, a, b = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        # Check H1: R is a UFD
        is_ufd = False
        if hasattr(R, 'is_UFD'):
            is_ufd = bool(R.is_UFD)
        elif R == sympy.ZZ:
            is_ufd = True
            
        # Check Conclusion
        # The ideal quotient (a) : (b) = { r in R | rb in (a) }
        # In a UFD, this is equal to the principal ideal (a / gcd(a, b)) 
        # for all pairs (a, b) EXCEPT when a = 0 and b = 0.
        # When a = 0 and b = 0, (0) : (0) = R = (1), but 0 / gcd(0, 0) is undefined (0/0).
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        
        g = sympy.gcd(a, b)
        
        if g == 0:
            # 0/0 is undefined, so the principal ideal (a / gcd(a, b)) is undefined.
            # Thus the equality fails.
            conclusion_holds = False
        else:
            # For any UFD, if gcd(a, b) != 0, the equality holds.
            conclusion_holds = True
                
        return [is_ufd, not conclusion_holds]
    except Exception:
        return [False, False]