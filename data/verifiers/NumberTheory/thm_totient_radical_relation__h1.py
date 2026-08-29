import sympy
import math

# Top-level setup (empty for Number Theory as per instructions)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H_1: rad(n) is the product of the distinct prime factors of n
    # This implies n is a non-zero integer where this definition is applicable.
    try:
        if isinstance(witness, bool):
            h1_ok = False
        else:
            n = int(witness)
            h1_ok = (n == witness) and (n != 0)
    except Exception:
        h1_ok = False

    # ¬Q: The conclusion phi(n) = (n / rad(n)) * phi(rad(n)) FAILS
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            n = int(witness)
            
            # rad(n) is the product of the distinct prime factors of |n|
            factors = sympy.primefactors(abs(n))
            rad_n = math.prod(factors) if factors else 1
            
            # phi(n) is the Euler totient function, typically defined for |n|
            phi_n = sympy.totient(abs(n))
            phi_rad = sympy.totient(rad_n)
            
            # Evaluate the right-hand side exactly
            rhs = sympy.Rational(n, rad_n) * phi_rad
            
            # The conclusion fails if the two sides are not equal
            neg_q_ok = bool(phi_n != rhs)
    except Exception:
        # If evaluation fails (e.g., undefined operations), the conclusion does not hold
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: rad(n) is the product of the distinct prime factors of n",
    "¬Q: phi(n) != (n / rad(n)) * phi(rad(n))"
]

N_HYP = 1
NEG_Q_INDEX = 1