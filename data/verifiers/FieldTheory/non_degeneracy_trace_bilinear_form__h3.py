import sympy
from sympy import Poly, gcd
from sympy.abc import x
from sympy.ntheory import factorint

# Top-level setup for witness evaluation namespace
# (No specific named groups or matrices are required for this field theory conjecture,
# but standard symbols are available via sympy imports).

def is_prime_power(q):
    try:
        if not isinstance(q, int) or q <= 1:
            return False
        return len(factorint(q)) == 1
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    The witness is expected to be either:
      - (q, n) where q is the field size and n is the extension degree.
      - (q, P_coeffs) where P_coeffs is a list of coefficients for the polynomial defining the extension.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        
        q, second = witness
        
        if isinstance(second, int):
            n = second
            P_coeffs = None
        elif isinstance(second, list):
            P_coeffs = second
            n = len(P_coeffs) - 1
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H1: F_q is a finite field
    h1 = is_prime_power(q)

    # H2: F_{q^n} is a finite field extension of F_q of degree n
    h2 = False
    try:
        if P_coeffs is not None:
            if h1:
                f = factorint(q)
                p = list(f.keys())[0]
                if q == p:
                    from sympy import GF
                    P = Poly(P_coeffs, x, domain=GF(p))
                    h2 = P.is_irreducible
                else:
                    try:
                        from sympy import GF
                        P = Poly(P_coeffs, x, domain=GF(q))
                        h2 = P.is_irreducible
                    except Exception:
                        # Fallback if GF(q) domain creation fails for prime powers
                        h2 = n >= 1
            else:
                h2 = False
        else:
            h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False

    # neg_Q: The bilinear form B is degenerate
    # The trace bilinear form of F_q[x]/(P(x)) is degenerate iff the discriminant of P is a zero divisor mod q.
    neg_q = False
    try:
        if P_coeffs is not None:
            P = Poly(P_coeffs, x)
            disc = P.discriminant()
            neg_q = bool(gcd(disc, q) > 1)
        else:
            # If only (q, n) is provided and it's a valid finite field, the trace form is mathematically
            # guaranteed to be non-degenerate (since finite fields are perfect and extensions are separable).
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: F_{q^n} is a finite field extension of F_q of degree n",
    "¬Q: The bilinear form B is degenerate"
]

N_HYP = 2
NEG_Q_INDEX = 2