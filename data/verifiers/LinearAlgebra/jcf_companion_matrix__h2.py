import sympy
from sympy import eye, zeros, Matrix
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    p = None
    C_raw = None
    
    # The witness can be a tuple (p(x), C) or just the matrix C.
    # If only C is provided, we assume p(x) is its characteristic polynomial.
    if isinstance(witness, tuple) and len(witness) == 2:
        p, C_raw = witness
    else:
        C_raw = witness

    C = None
    try:
        C = Matrix(C_raw)
    except Exception:
        pass

    if p is None and C is not None and getattr(C, 'is_square', False):
        try:
            p = C.charpoly(x).as_expr()
        except Exception:
            pass

    if p is not None:
        try:
            p = sympy.sympify(p)
        except Exception:
            pass

    # H_1: p(x) is a monic polynomial of degree n >= 1, and C is an n x n matrix
    h1 = False
    try:
        if p is not None and C is not None:
            poly_p = sympy.poly(p, x)
            deg = poly_p.degree()
            if poly_p.LC() == 1 and deg >= 1:
                if C.is_square and C.shape[0] == deg:
                    h1 = True
    except Exception:
        h1 = False

    # ¬Q: The Jordan canonical form of C does NOT contain exactly one Jordan block for each distinct root of p(x)
    neg_q = False
    try:
        if h1:
            poly_p = sympy.poly(p, x)
            roots = sympy.roots(p, x)
            
            # Ensure sympy was able to find all roots algebraically
            if sum(roots.values()) == poly_p.degree():
                q = True
                n_cols = C.shape[1]
                Id = eye(n_cols)
                
                for r in roots.keys():
                    # The number of Jordan blocks for an eigenvalue r is the geometric multiplicity,
                    # which equals the nullity of (C - r*I).
                    M = C - r * Id
                    nullity = n_cols - M.rank()
                    
                    if nullity != 1:
                        q = False
                        break
                        
                neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p(x) is a monic polynomial of degree n >= 1 and C is an n x n matrix",
    "¬Q: The Jordan canonical form of C does NOT contain exactly one Jordan block for each distinct root of p(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1