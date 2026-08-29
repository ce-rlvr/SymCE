import sympy
from sympy.ntheory import factorint, mobius, divisors

# Top-level setup
# (No specific named objects required for this number-theoretic/field-theoretic witness)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple (q, n)
        if isinstance(witness, tuple) and len(witness) == 2:
            q, n = witness
        else:
            # Fallback if only n is provided
            q, n = 2, witness
    except Exception:
        return [False, False]
        
    # H_1: F is a finite field with q elements (implies q is a prime power)
    try:
        q_val = int(q)
        if q_val < 2 or q_val != q:
            h1_ok = False
        else:
            f = factorint(q_val)
            h1_ok = len(f) == 1
    except Exception:
        h1_ok = False
        
    # ¬Q: The number of monic irreducible polynomials of degree n over F is NOT exactly the formula
    try:
        # Calculate the actual number of monic irreducible polynomials of degree n
        try:
            n_val = int(n)
            is_int_n = (n_val == n)
        except Exception:
            is_int_n = False

        if not is_int_n or n_val < 1:
            actual = 0
        else:
            ans = 0
            for d in divisors(n_val):
                ans += mobius(d) * (q_val ** (n_val // d))
            actual = ans // n_val
            
        # Evaluate the formula given in the conclusion
        try:
            ans = 0
            for d in divisors(n):
                ans += mobius(d) * (sympy.Rational(q) ** sympy.Rational(n, d))
            formula = ans / sympy.Rational(n)
            neg_q_ok = (actual != formula)
        except Exception:
            # If the formula is undefined (e.g., division by zero or divisors of 0),
            # then the number is not exactly the formula.
            neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a finite field with q elements",
    "¬Q: The number of monic irreducible polynomials of degree n is not exactly the formula"
]

N_HYP = 1
NEG_Q_INDEX = 1