import sympy
from sympy.ntheory import factorint

# Top-level setup for potential witness expressions
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to represent the ring of integers of Q(sqrt(d)).
    It can be provided as a square-free integer d, a minimal polynomial (e.g., x**2 + 5),
    or a field generator (e.g., sympy.sqrt(-5)).
    """
    d = None
    try:
        # Extract the core value if wrapped in a tuple/list
        if isinstance(witness, (tuple, list)):
            val = witness[0]
        else:
            val = witness
            
        # Attempt to extract 'd' if the witness is a sympy Expression (like a polynomial or sqrt)
        if isinstance(val, sympy.Expr):
            try:
                poly = sympy.poly(val)
                if poly is not None and poly.degree() == 2:
                    coeffs = poly.all_coeffs()
                    a, b, c = coeffs
                    delta = int(b**2 - 4*a*c)
                    factors = factorint(abs(delta))
                    d_val = 1 if delta > 0 else -1
                    for p, exp in factors.items():
                        if exp % 2 == 1:
                            d_val *= p
                    d = d_val
            except Exception:
                pass
                
            if d is None:
                try:
                    sq = val**2
                    if sq.is_Integer or sq.is_Rational:
                        delta = int(sq)
                        factors = factorint(abs(delta))
                        d_val = 1 if delta > 0 else -1
                        for p, exp in factors.items():
                            if exp % 2 == 1:
                                d_val *= p
                        d = d_val
                except Exception:
                    pass
                    
        # Fallback: treat the witness directly as the integer d
        if d is None:
            d = int(val)
            
        if d in (0, 1):
            h1 = False
        else:
            factors = factorint(abs(d))
            h1 = all(v == 1 for v in factors.values())
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1 and d is not None:
            # A ring of integers of Q(sqrt(d)) is norm-Euclidean if and only if d is in one of these sets.
            # (Chatland-Davenport theorem for real quadratic fields, Stark for imaginary)
            norm_euclidean_imaginary = {-1, -2, -3, -7, -11}
            norm_euclidean_real = {2, 3, 5, 6, 7, 11, 13, 17, 19, 21, 29, 33, 37, 41, 57, 73}
            
            if d < 0:
                if d not in norm_euclidean_imaginary:
                    neg_q = True
            elif d > 0:
                if d not in norm_euclidean_real:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Witness represents the ring of integers of Q(sqrt(d)) for a square-free integer d",
    "¬Q: The ring is not a Euclidean domain with Euclidean function N"
]

N_HYP = 1
NEG_Q_INDEX = 1