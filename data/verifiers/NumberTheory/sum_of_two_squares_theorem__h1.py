import sympy
from sympy.ntheory import factorint

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "n can be expressed as the sum of two squares of integers if and only if 
    every prime factor p of n with p = 3 (mod 4) has an even exponent in the 
    prime factorization of n"
    """
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        n = int(witness)
    except Exception:
        return [False]
        
    # Evaluate LHS: n can be expressed as the sum of two squares of integers
    try:
        lhs = False
        if n >= 0:
            if n > 10**6:
                # For very large n, use the known true theorem for positive integers to avoid timeout
                lhs = True
                for p, e in factorint(n).items():
                    if p > 1 and p % 4 == 3 and e % 2 != 0:
                        lhs = False
                        break
            else:
                # For small n, check directly
                limit = int(sympy.integer_nthroot(n, 2)[0])
                for a in range(limit + 1):
                    b2 = n - a * a
                    b = int(sympy.integer_nthroot(b2, 2)[0])
                    if b * b == b2:
                        lhs = True
                        break
    except Exception:
        lhs = False
        
    # Evaluate RHS: every prime factor p of n with p = 3 (mod 4) has an even exponent
    try:
        rhs = True
        if n != 0:
            factors = factorint(n)
            for p, e in factors.items():
                if p > 1 and p % 4 == 3:
                    if e % 2 != 0:
                        rhs = False
                        break
        else:
            # factorint(0) is {0: 1}, which has no prime factors
            rhs = True
    except Exception:
        rhs = False
        
    # The conjecture states LHS <-> RHS.
    # The negated conclusion is True when the equivalence fails (i.e., LHS != RHS).
    try:
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: n can be expressed as the sum of two squares iff every prime factor p = 3 (mod 4) has an even exponent fails"
]

N_HYP = 0
NEG_Q_INDEX = 0