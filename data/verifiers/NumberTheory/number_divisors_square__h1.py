import sympy
from sympy.ntheory import divisor_count, primefactors, divisors

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness and ensure it is an integer
        n = sympy.sympify(witness)
        if not n.is_integer:
            return [False]
        n = int(n)
        
        # Evaluate the left-hand side: d(n^2)
        lhs = divisor_count(n**2)
        
        # Evaluate the right-hand side: sum_{k|n} 2^{\omega(k)}
        # where \omega(k) is the number of distinct prime factors of k.
        rhs = sum(2**len(primefactors(k)) for k in divisors(n))
        
        # The negated conclusion is True if the equality FAILS
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: d(n^2) != sum_{k|n} 2^omega(k)"
]

N_HYP = 0
NEG_Q_INDEX = 0