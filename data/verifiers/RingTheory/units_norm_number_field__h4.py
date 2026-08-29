import sympy
from sympy import minpoly, I, Rational, Poly, eye, zeros
from sympy.abc import x

# Standard linear algebra objects for potential use in witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The element alpha is a unit in O_K if and only if N_{K/Q}(alpha) = 1 or N_{K/Q}(alpha) = -1."
    
    The missing hypothesis is that alpha must be an element of O_K (an algebraic integer).
    Without it, an algebraic number can have norm +/- 1 but not be a unit in O_K 
    (because it is not in O_K to begin with).
    """
    # Extract alpha if witness is provided as a tuple (e.g., (K, alpha))
    if isinstance(witness, (tuple, list)):
        if len(witness) > 0:
            witness = witness[-1]
        else:
            return [False, False]

    # H_1: alpha is an algebraic number
    try:
        if getattr(witness, 'is_Matrix', False):
            h1 = False
        else:
            # minpoly succeeds if and only if the element is an algebraic number
            p_expr = minpoly(witness, x)
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: The equivalence fails
    try:
        if getattr(witness, 'is_Matrix', False):
            neg_q = False
        elif witness == 0:
            is_unit = False
            norm_pm1 = False
            neg_q = bool(is_unit != norm_pm1)
        else:
            # Compute minimal polynomial of alpha
            p_expr = minpoly(witness, x)
            p_poly = Poly(p_expr, x)
            
            # alpha is an algebraic integer iff its minimal polynomial over Q has integer coefficients
            is_alg_int = all(c.is_integer for c in p_poly.all_coeffs())
            
            # Compute minimal polynomial of 1/alpha
            inv_p_expr = minpoly(1/witness, x)
            inv_p_poly = Poly(inv_p_expr, x)
            
            # 1/alpha is an algebraic integer iff its minimal polynomial over Q has integer coefficients
            is_inv_alg_int = all(c.is_integer for c in inv_p_poly.all_coeffs())
            
            # alpha is a unit in O_K iff both alpha and 1/alpha are algebraic integers
            is_unit = is_alg_int and is_inv_alg_int
            
            # The norm of alpha from Q(alpha) to Q is (-1)^d * constant_term
            d = p_poly.degree()
            const_term = p_poly.all_coeffs()[-1]
            norm = ((-1)**d) * const_term
            
            # Check if norm is 1 or -1
            norm_pm1 = (norm == 1 or norm == -1)
            
            # The conclusion fails if the equivalence does not hold
            neg_q = bool(is_unit != norm_pm1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is an algebraic number",
    "¬Q: alpha is a unit in O_K iff N_{K/Q}(alpha) = +/- 1 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1