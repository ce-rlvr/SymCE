import sympy
from sympy import lcm, Rational
from sympy.ntheory import totient, divisors

CONDITION_LABELS = [
    "¬Q: The equation sum_{k=1}^n lcm(k, n) == n/2 * (1 + sum_{d|n} d * phi(d)) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        
        if not n.is_Integer:
            neg_q = True
        else:
            # Evaluate LHS: sum_{k=1}^n lcm(k, n)
            if n >= 1:
                lhs = sum(lcm(k, n) for k in range(1, int(n) + 1))
            else:
                lhs = 0
                
            # Evaluate RHS: n/2 * (1 + sum_{d|n} d * phi(d))
            if n == 0:
                # Divisors of 0 are undefined, so the formula is undefined and equality fails
                neg_q = True
            else:
                divs = divisors(n)
                rhs_sum = sum(d * totient(d) for d in divs)
                rhs = Rational(n, 2) * (1 + rhs_sum)
                
                neg_q = bool(lhs != rhs)
                
    except Exception:
        neg_q = False

    return [neg_q]