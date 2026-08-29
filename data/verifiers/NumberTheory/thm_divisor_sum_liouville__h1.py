import sympy
import math

def conditions(witness):
    try:
        n = witness
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 0
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            divs = sympy.divisors(n)
            
            def liouville(x):
                if x == 1:
                    return 1
                return (-1) ** sum(sympy.factorint(x).values())
            
            lhs = sum(liouville(d) for d in divs)
            is_sq = (math.isqrt(n)**2 == n)
            rhs = 1 if is_sq else 0
            
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sum_{d|n} lambda(d) != (1 if n is a perfect square else 0)"
]

N_HYP = 1
NEG_Q_INDEX = 1