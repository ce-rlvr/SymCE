import sympy
import math

def conditions(witness):
    try:
        n_sym = sympy.S(witness)
        
        # P(n): has a solution in integers for x^2 + y^2 + z^2 = n
        def has_solution(n_val):
            if n_val.is_integer is not True:
                return False
            n_int = int(n_val)
            if n_int < 0:
                return False
            limit = int(math.isqrt(n_int))
            for x in range(limit + 1):
                for y in range(x, limit + 1):
                    z2 = n_int - x*x - y*y
                    if z2 < 0:
                        break
                    z = int(math.isqrt(z2))
                    if z*z == z2:
                        return True
            return False
            
        # R(n): cannot be expressed as 4^a(8b+7) for non-negative integers a, b
        def cannot_express(n_val):
            if n_val.is_integer is not True:
                return True
            n_int = int(n_val)
            if n_int < 0:
                return True
            if n_int == 0:
                return True
            while n_int % 4 == 0:
                n_int //= 4
            if n_int % 8 == 7:
                return False
            return True
            
        p = has_solution(n_sym)
        r = cannot_express(n_sym)
        
        # The conclusion is P(n) <==> R(n). It fails if P(n) != R(n).
        neg_q = bool(p != r)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence between having a 3-square sum and not being of the form 4^a(8b+7) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0