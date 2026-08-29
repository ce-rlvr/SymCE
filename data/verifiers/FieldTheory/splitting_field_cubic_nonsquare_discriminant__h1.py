import sympy
from sympy import Poly, Symbol

# Top-level setup
# No specific named objects are required for this Field Theory conjecture,
# but we define standard symbols that might be used in a witness.
x, y, t = sympy.symbols('x y t')

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible polynomial of degree 3",
    "H_2: The discriminant of f(x) is not a perfect square in F",
    "¬Q: The degree of the splitting field of f(x) over F is NOT exactly 6"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness (expected to be a sympy Poly or an expression convertible to one),
    evaluates the hypotheses and the negated conclusion.
    """
    try:
        # Extract polynomial from witness
        if isinstance(witness, tuple):
            poly = witness[0]
        else:
            poly = witness
            
        if not isinstance(poly, Poly):
            poly = Poly(poly)
            
        domain = poly.domain
        
        # H_1: f(x) is an irreducible polynomial of degree 3
        try:
            h1 = (poly.degree() == 3) and poly.is_irreducible
        except Exception:
            h1 = False
            
        # H_2: The discriminant of f(x) is not a perfect square in F
        try:
            disc = poly.discriminant()
            
            # Check if disc is a perfect square in the domain
            if domain.is_QQ:
                is_sq = sympy.sqrt(disc).is_Rational
            elif domain.is_ZZ:
                is_sq = sympy.sqrt(disc).is_integer
            elif hasattr(domain, 'is_square'):
                is_sq = domain.is_square(disc)
            else:
                # Generic fallback: check if x^2 - disc has roots in the domain
                if disc == 0:
                    is_sq = True
                else:
                    z = Symbol('z')
                    q = Poly(z**2 - disc, z, domain=domain)
                    roots = q.ground_roots()
                    is_sq = len(roots) > 0
                    
            h2 = not is_sq
        except Exception:
            h2 = False
            
        # ¬Q: The degree of the splitting field of f(x) over F is NOT exactly 6
        try:
            # Compute the degree of the splitting field
            if domain.is_FiniteField:
                # For finite fields, the splitting field of an irreducible degree n polynomial has degree n
                deg = poly.degree() if h1 else 0
            elif domain.is_QQ:
                # Over Q, the degree of the splitting field of an irreducible cubic
                # is 6 if the discriminant is not a square, and 3 if it is.
                if h1:
                    deg = 6 if h2 else 3
                else:
                    deg = 0
            else:
                # For general fields, if it's an irreducible cubic:
                # If it's inseparable (disc == 0), the splitting field has degree 3.
                # If it's separable, degree is 6 if disc is not a square, else 3.
                if h1:
                    if disc == 0:
                        deg = 3
                    else:
                        deg = 6 if h2 else 3
                else:
                    deg = 0
                    
            neg_q = (deg != 6)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
        
    except Exception:
        return [False, False, False]