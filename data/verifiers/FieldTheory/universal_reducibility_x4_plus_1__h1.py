import sympy
from sympy import Symbol

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "The polynomial x^4 + 1 is reducible over F_q".
    
    The true theorem is that x^4 + 1 is reducible over F_p for all primes p.
    When the hypothesis "p is prime" is dropped, the conjecture becomes false
    because x^4 + 1 is irreducible over Z/qZ for any q that is a multiple of 4.
    (Note: F_q here is interpreted as Z/qZ, a common abuse of notation in this context).
    """
    # Handle the case where the witness might be passed as the rational field
    if witness in ['Q', 'QQ', sympy.QQ]:
        return [True]
        
    try:
        q = int(witness)
    except Exception:
        return [False]
        
    if q <= 1:
        return [False]
        
    try:
        if q <= 1000:
            is_red = False
            # Check for a linear factor (i.e., a root mod q)
            for val in range(q):
                if (val**4 + 1) % q == 0:
                    is_red = True
                    break
            
            if not is_red:
                # Check for quadratic factors
                # x^4 + 1 = (x^2 + ax + b)(x^2 + cx + d) mod q
                # Equating coefficients gives:
                # c = -a mod q
                # d = a^2 - b mod q
                # a(d - b) = 0 mod q
                # bd = 1 mod q
                for a in range(q):
                    for b in range(q):
                        d = (a**2 - b) % q
                        if (a * (d - b)) % q == 0:
                            if (b * d) % q == 1:
                                is_red = True
                                break
                    if is_red:
                        break
        else:
            # For large q, use the mathematical property:
            # x^4 + 1 is reducible mod q if and only if q is not a multiple of 4.
            is_red = (q % 4 != 0)
            
        neg_q = not is_red
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The polynomial x^4 + 1 is irreducible over F_q"
]
N_HYP = 0
NEG_Q_INDEX = 0