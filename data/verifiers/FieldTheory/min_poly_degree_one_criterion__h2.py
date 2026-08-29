import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy import QQ, RR, ZZ, CC

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    Hypotheses:
      - F is a field
      - α is algebraic over F
    Conclusion:
      The minimal polynomial of α over F has degree 1 if and only if α ∈ F
    """
    try:
        F, alpha = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False
        
    # H_2: α is algebraic over F
    try:
        x = sympy.Symbol('x')
        if isinstance(alpha, sympy.MatrixBase):
            # For matrices (elements of an F-algebra), compute the minimal polynomial
            # and check if all its coefficients lie in F.
            p = alpha.minpoly(x)
            poly = sympy.Poly(p, x)
            h2 = all(c in F for c in poly.coeffs())
        else:
            # For scalars, use sympy's minpoly with the specified domain.
            p = sympy.minpoly(alpha, x, domain=F)
            poly = sympy.Poly(p, x)
            h2 = True
    except Exception:
        h2 = False
        poly = None

    # ¬Q: The minimal polynomial of α over F has degree 1 if and only if α ∈ F (must FAIL)
    # This means the biconditional is false, which is equivalent to XOR.
    try:
        if poly is not None:
            deg_is_1 = (poly.degree() == 1)
            
            # Safely check if alpha is in F
            if isinstance(alpha, (sympy.MatrixBase, list, tuple)):
                alpha_in_F = False
            else:
                try:
                    alpha_in_F = bool(alpha in F)
                except Exception:
                    alpha_in_F = False
                    
            neg_q = bool(deg_is_1 != alpha_in_F)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: α is algebraic over F",
    "¬Q: The minimal polynomial of α over F has degree 1 XOR α ∈ F"
]

N_HYP = 2
NEG_Q_INDEX = 2