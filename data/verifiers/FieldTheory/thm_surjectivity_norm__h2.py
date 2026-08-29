import sympy
from sympy import isprime, Poly, Matrix, GF, sympify
from sympy.abc import x
from itertools import product

# Top-level setup
# The witness is expected to be a tuple (p, f) where p is a prime integer 
# defining the finite field F = GF(p), and f is a polynomial in x (or a list of coefficients)
# defining the finite F-algebra E = F[x]/(f).

def conditions(witness):
    try:
        p, f = witness
    except Exception:
        return [False, False]
    
    try:
        if hasattr(p, 'p'):
            p = p.p
        p = int(p)
        h1 = isprime(p)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            if isinstance(f, list):
                poly_f = Poly(f, x, domain=GF(p))
            else:
                poly_f = Poly(sympify(f), x, domain=GF(p))
            
            d = poly_f.degree()
            # If degree is less than 1, it's not a valid algebra extension.
            # We also limit the size of the algebra to prevent TLE.
            if d < 1 or p**d > 2000:
                neg_q = False
            else:
                norms = set()
                # Iterate over all elements of E = F[x]/(f)
                for coeffs in product(range(p), repeat=d):
                    if all(c == 0 for c in coeffs):
                        continue  # Skip the zero element
                    
                    # Construct the element g in E
                    g = Poly(sum(c * x**i for i, c in enumerate(coeffs)), x, domain=GF(p))
                    
                    # Construct the matrix of the multiplication map L_g: E -> E
                    matrix = []
                    for i in range(d):
                        term = g * Poly(x**i, x, domain=GF(p))
                        _, rem = term.div(poly_f)
                        rem_poly = Poly(rem.as_expr(), x)
                        # Extract coefficients of the remainder to form the matrix row
                        rem_coeffs = [int(rem_poly.nth(j)) % p for j in range(d)]
                        matrix.append(rem_coeffs)
                    
                    M = Matrix(matrix)
                    # The norm is the determinant of the multiplication matrix
                    norm = int(M.det()) % p
                    norms.add(norm)
                
                # The non-zero elements of F are 1, 2, ..., p-1
                target = set(range(1, p))
                
                # neg_q is True if the norm map is NOT surjective onto the non-zero elements of F
                neg_q = not target.issubset(norms)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "¬Q: The field norm map from E to F does not map the non-zero elements of E surjectively onto the non-zero elements of F"
]

N_HYP = 1
NEG_Q_INDEX = 1