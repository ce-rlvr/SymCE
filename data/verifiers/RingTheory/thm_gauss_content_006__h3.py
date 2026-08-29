import sympy
from sympy import Poly, symbols, Expr

# Top-level setup
X, Y, Z = symbols('X Y Z')

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f_expr, varX, varY = witness
                f = Poly(f_expr, varX, varY)
            elif len(witness) == 4:
                f_expr, varX, varY, domain = witness
                f = Poly(f_expr, varX, varY, domain=domain)
            else:
                return [False, False, False]
        elif isinstance(witness, Expr):
            f = Poly(witness, X, Y)
            varX, varY = X, Y
        else:
            f = witness
            if not hasattr(f, 'gens') or len(f.gens) != 2:
                return [False, False, False]
            varX, varY = f.gens
            
        domain = f.domain
        
        # H_1: R is a Unique Factorization Domain
        h1 = domain.is_UFD
        if h1 is None:
            h1 = False
            
        # H_2: f in R[X,Y] is a non-zero polynomial
        h2 = not f.is_zero
        
        # Compute the total content of f as a polynomial in R[X,Y]
        tot_content = f.content()
        
        # Compute c_Y(f), the content of f with respect to Y
        # View f as a polynomial in Y over R[X]
        f_Y = Poly(f.as_expr(), varY)
        coeffs_Y = f_Y.all_coeffs()
        
        # c_Y(f) is the gcd of the coefficients of f_Y in R[X]
        c_Y = Poly(coeffs_Y[0], varX, domain=domain)
        for c in coeffs_Y[1:]:
            c_Y = c_Y.gcd(Poly(c, varX, domain=domain))
            
        # Compute the content of c_Y(f) as a polynomial in R[X]
        c_c_Y = c_Y.content()
        
        # not Q: The content of c_Y(f) in R[X] is NOT equal to the total content of f in R[X,Y]
        neg_q = (c_c_Y != tot_content)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial",
    "¬Q: The content of c_Y(f) is not equal to the total content of f"
]

N_HYP = 2
NEG_Q_INDEX = 2