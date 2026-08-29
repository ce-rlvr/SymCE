import sympy
from sympy import Matrix, oo, degree, minpoly
from sympy.abc import x
from sympy import QQ

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, Matrix) and witness.is_square:
            h1 = True
            n = witness.shape[0]
            min_poly = witness.minimal_polynomial(x)
            deg_alpha = degree(min_poly, x)
            
            if deg_alpha != 0 and n % deg_alpha != 0:
                neg_q = True

        elif isinstance(witness, tuple) and len(witness) == 2:
            K, alpha = witness
            
            if type(K).__name__ == 'FractionField':
                try:
                    if hasattr(K, 'from_expr'):
                        K.from_expr(alpha)
                        h1 = True
                    else:
                        h1 = str(alpha) in [str(g) for g in K.gens]
                except Exception:
                    h1 = False
                    
                if h1:
                    neg_q = True
                    
            elif type(K).__name__ == 'AlgebraicField':
                try:
                    if hasattr(K, 'from_expr'):
                        K.from_expr(alpha)
                        h1 = True
                    else:
                        h1 = True
                except Exception:
                    h1 = False
                    
                if h1:
                    deg_K = K.degree()
                    poly_alpha = minpoly(alpha)
                    deg_alpha = degree(poly_alpha, x)
                    
                    if deg_alpha != 0 and deg_K % deg_alpha != 0:
                        neg_q = True

    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is an element of K",
    "¬Q: The degree of F(alpha) over F does not divide the degree of K over F"
]

N_HYP = 1
NEG_Q_INDEX = 1