import sympy
from sympy import gcd, lcm

# Top-level setup
# (No named bindings needed for this Number Theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
        lhs = lcm(a, gcd(b, c))
        rhs = gcd(lcm(a, b), lcm(a, c))
        
        # Check if the conclusion fails (i.e., LHS is not equal to RHS)
        if hasattr(lhs, 'equals') and callable(lhs.equals):
            neg_q = not bool(lhs.equals(rhs))
        else:
            neg_q = bool(lhs != rhs)
            
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: lcm(a, gcd(b, c)) != gcd(lcm(a, b), lcm(a, c))"
]

N_HYP = 0
NEG_Q_INDEX = 0