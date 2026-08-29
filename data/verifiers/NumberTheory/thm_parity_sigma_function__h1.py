import sympy
import math

def conditions(witness):
    if isinstance(witness, bool):
        return [False, False]
        
    try:
        n = int(witness)
        if n == 0 or n != witness:
            h1 = False
        else:
            # Verify that sigma(n) can be computed (sum of positive divisors)
            s = sympy.divisor_sigma(n)
            h1 = True
    except Exception:
        h1 = False

    try:
        n = int(witness)
        if n == 0 or n != witness:
            neg_q = False
        else:
            s = int(sympy.divisor_sigma(n))
            is_odd = (s % 2 != 0)
            
            def is_ps(x):
                if x < 0: 
                    return False
                r = math.isqrt(x)
                return r * r == x
                
            def is_twice_ps(x):
                if x < 0 or x % 2 != 0: 
                    return False
                return is_ps(x // 2)
                
            rhs = is_ps(n) or is_twice_ps(n)
            
            # The conclusion fails if the parity of sigma(n) does not match the condition
            neg_q = (is_odd != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: sigma(n) is the sum of the positive divisors of n",
    "¬Q: sigma(n) being odd is not equivalent to n being a perfect square or twice a perfect square"
]

N_HYP = 1
NEG_Q_INDEX = 1