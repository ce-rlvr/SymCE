import sympy
from sympy import Poly, Symbol

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, g) or (F, f, g) where f and g are expressions in x.
    """
    if isinstance(witness, tuple):
        if len(witness) == 3:
            F, f, g = witness
        elif len(witness) == 2:
            f, g = witness
        else:
            return [False, False, False]
    else:
        return [False, False, False]
    
    poly_f = None
    poly_g = None
    
    # H_1: F is a field
    # We evaluate the polynomials over QQ to ensure we are working over a field.
    try:
        poly_f = Poly(f, x, domain='QQ')
        poly_g = Poly(g, x, domain='QQ')
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: f(x) is a non-zero polynomial
    try:
        h2_ok = False
        if poly_f is not None:
            h2_ok = not poly_f.is_zero
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion fails at the witness.
    # Conclusion: g(x) + <f(x)> is a zero divisor iff gcd(f(x), g(x)) != 1
    try:
        neg_q_ok = False
        if poly_f is not None and poly_g is not None:
            # Compute remainder of g divided by f
            _, rem_poly = poly_g.div(poly_f)
            is_zero_coset = rem_poly.is_zero
            
            # Compute gcd(f, g)
            d_poly = poly_f.gcd(poly_g)
            deg_d = d_poly.degree()
            
            # A zero divisor must be a non-zero element in the factor ring.
            # If it is non-zero, it is a zero divisor iff there exists a non-zero h + <f>
            # such that g*h = 0 mod f. This is true iff deg(gcd(f, g)) > 0.
            if is_zero_coset:
                is_zd = False
            else:
                is_zd = (deg_d > 0)
                
            # In F[x], gcd != 1 is equivalent to deg(gcd) > 0 (since gcd is monic)
            gcd_not_1 = (deg_d > 0)
            
            # The conjecture claims is_zd == gcd_not_1
            q = (is_zd == gcd_not_1)
            neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a non-zero polynomial",
    "¬Q: g(x) + <f(x)> is a zero divisor iff gcd(f(x), g(x)) != 1 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2