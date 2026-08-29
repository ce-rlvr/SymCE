import sympy
from sympy import Poly, discriminant

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "f(x) is irreducible over R if and only if either deg(f) = 1, or deg(f) = 2 and the discriminant of f(x) is strictly negative."
    
    The conjecture drops the hypothesis that f(x) must be a polynomial with real coefficients.
    """
    try:
        p = Poly(witness, x)
        
        # Evaluate LHS: f(x) is irreducible over R
        # To be irreducible over R, it must be a polynomial in R[x].
        is_real_poly = True
        for c in p.coeffs():
            # If is_real is False or None, we cannot confirm it's in R[x]
            if not getattr(c, 'is_real', False):
                is_real_poly = False
                break
                
        if is_real_poly:
            d = p.degree()
            if d == 1:
                lhs = True
            elif d == 2:
                disc = discriminant(witness, x)
                try:
                    lhs = bool(getattr(disc, 'is_real', False) and disc < 0)
                except TypeError:
                    lhs = False
            else:
                lhs = False
        else:
            lhs = False
            
    except Exception:
        lhs = False

    try:
        p = Poly(witness, x)
        d = p.degree()
        
        # Evaluate RHS: deg(f) = 1, or deg(f) = 2 and discriminant of f(x) is strictly negative
        if d == 1:
            rhs = True
        elif d == 2:
            disc = discriminant(witness, x)
            try:
                rhs = bool(getattr(disc, 'is_real', False) and disc < 0)
            except TypeError:
                rhs = False
        else:
            rhs = False
    except Exception:
        rhs = False

    # The conclusion is an iff statement. It fails if LHS != RHS.
    neg_q = (lhs != rhs)
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: f(x) is irreducible over R iff deg(f)=1 or (deg(f)=2 and disc<0) FAILS"
]

N_HYP = 0
NEG_Q_INDEX = 0