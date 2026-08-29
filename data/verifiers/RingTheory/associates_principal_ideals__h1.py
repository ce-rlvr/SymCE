import sympy
from sympy import Poly

# Top-level setup: named object bindings that the witness expression may reference.
# We use the polynomial ring Z[x] / (n*x) as the domain for our counterexample.
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    
    The witness is expected to be a tuple: (n, A, B, C, D)
    representing elements in the ring R = Z[x] / (n*x), where:
      - n is a square-free integer > 1
      - A and B are the elements a and b
      - C and D are elements such that A = C * B and B = D * A in R
    """
    try:
        n, A, B, C, D = witness
    except Exception:
        return [False, False]
        
    # H_1: a and b are elements of R
    # We verify that n is a valid square-free integer (which guarantees the only units in R are 1 and -1)
    # and that A, B, C, D are valid polynomials in x over the integers.
    try:
        if not isinstance(n, (int, sympy.Integer)) or int(n) <= 1:
            h1 = False
        else:
            n_int = int(n)
            # Check that n is square-free
            factors = sympy.factorint(n_int)
            if any(v > 1 for v in factors.values()):
                h1 = False
            else:
                # Check that A, B, C, D are polynomials in x with integer coefficients
                Poly(A, x, domain='ZZ')
                Poly(B, x, domain='ZZ')
                Poly(C, x, domain='ZZ')
                Poly(D, x, domain='ZZ')
                h1 = True
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion "a and b are associates if and only if (a) = (b)" FAILS.
    # This means (a) = (b) is True, but a and b are NOT associates.
    try:
        n_int = int(n)
        
        def eq_in_R(p1, p2):
            """Check if p1 == p2 in Z[x] / (n*x)."""
            diff = Poly(p1 - p2, x, domain='ZZ')
            coeffs = diff.all_coeffs()
            if not coeffs:
                return True
            # all_coeffs returns coefficients from highest degree to lowest
            coeffs = coeffs[::-1] 
            # Constant term must be exactly 0
            if coeffs[0] != 0:
                return False
            # Higher degree terms must be 0 modulo n
            for c in coeffs[1:]:
                if c % n_int != 0:
                    return False
            return True

        # Check if (A) = (B) by verifying the provided multipliers C and D
        ideal_eq = eq_in_R(A, C * B) and eq_in_R(B, D * A)
        
        # Check if A and B are associates.
        # Since n is square-free, the only units in Z[x] / (n*x) are 1 and -1.
        # Thus, A and B are associates if and only if A = B or A = -B in R.
        associates = eq_in_R(A, B) or eq_in_R(A, -B)
        
        # The conclusion fails if they generate the same ideal but are NOT associates.
        neg_q = bool(ideal_eq and not associates)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "¬Q: a and b are associates if and only if (a) = (b) FAILS"
]
N_HYP = 1
NEG_Q_INDEX = 1