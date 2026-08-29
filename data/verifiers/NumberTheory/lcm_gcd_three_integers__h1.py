import sympy
from sympy import lcm, gcd

CONDITION_LABELS = [
    "¬Q: lcm(a, b, c) != (a*b*c*gcd(a,b,c)) / (gcd(a,b)*gcd(b,c)*gcd(c,a))"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False]
        a, b, c = witness
        
        # Ensure the witness elements are integers
        if isinstance(a, bool) or isinstance(b, bool) or isinstance(c, bool):
            return [False]
            
        if int(a) != a or int(b) != b or int(c) != c:
            return [False]
            
        a = int(a)
        b = int(b)
        c = int(c)
        
        lhs = lcm(a, lcm(b, c))
        
        num = a * b * c * gcd(a, gcd(b, c))
        den = gcd(a, b) * gcd(b, c) * gcd(c, a)
        
        if den == 0:
            # Division by zero means the formula is undefined, so equality fails
            neg_q = True
        else:
            # Check if the equality fails
            neg_q = (lhs * den != num)
            
    except Exception:
        neg_q = False
        
    return [neg_q]