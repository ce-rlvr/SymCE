import sympy

CONDITION_LABELS = [
    "¬Q: sum_{d|n} mu(d) log(n/d) != Lambda(n)"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness) -> list[bool]:
    try:
        n = sympy.sympify(witness)
        
        # Check if the witness is an integer
        try:
            if n == int(n):
                n = int(n)
            else:
                # If n is not an integer, the terms are undefined, so the equality fails.
                return [True]
        except Exception:
            # If conversion to int fails (e.g., for symbols), it's not a valid integer.
            return [True]
            
        # The identity holds for all integers n >= 1.
        # For n <= 0, the von Mangoldt function is undefined and the equality fails.
        if n <= 0:
            return [True]
            
        # Compute LHS: sum_{d|n} mu(d) log(n/d)
        divs = sympy.divisors(n)
        lhs = sympy.S.Zero
        for d in divs:
            lhs += sympy.mobius(d) * sympy.log(sympy.Rational(n, d))
            
        # Compute RHS: Lambda(n) (von Mangoldt function)
        if n == 1:
            rhs = sympy.S.Zero
        else:
            factors = sympy.factorint(n)
            if len(factors) == 1:
                p = list(factors.keys())[0]
                rhs = sympy.log(p)
            else:
                rhs = sympy.S.Zero
                
        # Check if LHS equals RHS
        diff = sympy.simplify(sympy.logcombine(lhs - rhs, force=True))
        neg_q = bool(diff != 0)
        
    except Exception:
        # If any unexpected error occurs during evaluation, return False as a safe fallback
        neg_q = False
        
    return [neg_q]