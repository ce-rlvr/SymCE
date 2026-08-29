import sympy
from sympy import symbols, Poly, groebner, reduced, Rational, Integer

# Top-level setup: define the polynomial ring variables
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a list of polynomials in x, y, z generating an ideal I.
    """
    # H_1: R is a graded ring
    # We fix R = Q[x, y, z] with the standard grading. We just verify the witness 
    # is a valid non-empty list of polynomials in R.
    h1_ok = False
    try:
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            valid = True
            for f in witness:
                # Check if f can be interpreted as a polynomial in x, y, z
                Poly(f, x, y, z)
            h1_ok = valid
    except Exception:
        h1_ok = False

    # ¬Q: R/I does not have a natural grading such that the canonical projection is a graded homomorphism.
    # This happens if and only if the ideal I is NOT a homogeneous ideal.
    # An ideal is homogeneous iff the homogeneous components of its generators belong to the ideal.
    neg_q = False
    try:
        if h1_ok:
            # Compute the Groebner basis of the ideal to check for ideal membership
            G = list(groebner(witness, x, y, z))
            is_homog = True
            
            for f in witness:
                f_poly = Poly(f, x, y, z)
                components = {}
                
                # Extract homogeneous components of the generator f
                for monom, coeff in f_poly.terms():
                    deg = sum(monom)
                    if deg not in components:
                        components[deg] = 0
                    
                    term = coeff
                    for v, p in zip((x, y, z), monom):
                        term *= v**p
                    components[deg] += term
                
                # Check if every homogeneous component belongs to the ideal I
                for comp in components.values():
                    _, rem = reduced(comp, G, x, y, z)
                    if rem != 0:
                        is_homog = False
                        break
                
                if not is_homog:
                    break
                    
            neg_q = not is_homog
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a graded ring",
    "¬Q: R/I does not have a natural grading such that the projection is a graded ring homomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1