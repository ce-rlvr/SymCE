import sympy
from sympy import Matrix, eye, zeros, Poly
from sympy.abc import x

# Standard bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_matrix(witness):
    """
    Attempts to interpret the witness as a square matrix or the minimal polynomial
    of an algebraic element, returning the corresponding matrix representation.
    """
    if getattr(witness, 'is_Matrix', False) or isinstance(witness, sympy.MatrixBase):
        if witness.shape[0] == witness.shape[1] and witness.shape[0] <= 20:
            return witness
            
    if isinstance(witness, list):
        try:
            M = sympy.Matrix(witness)
            if M.shape[0] == M.shape[1] and M.shape[0] <= 20:
                return M
        except Exception:
            pass
            
    try:
        poly = sympy.Poly(witness)
        if not poly.is_univariate:
            return None
        coeffs = poly.all_coeffs()
        if not coeffs:
            return None
        if coeffs[0] != 1:
            poly = sympy.Poly(poly.as_expr() / coeffs[0], poly.gens[0])
            coeffs = poly.all_coeffs()
        d = len(coeffs) - 1
        if 0 < d <= 20:
            # Construct the companion matrix for the polynomial
            M = sympy.zeros(d, d)
            for i in range(d - 1):
                M[i + 1, i] = 1
            for i in range(d):
                M[i, d - 1] = -coeffs[d - i]
            return M
    except Exception:
        pass
        
    return None

def minpoly_degree(M):
    """
    Computes the degree of the minimal polynomial of a square matrix M.
    """
    if M is None:
        return -1
    d = M.shape[0]
    if d == 0:
        return 0
        
    vecs = []
    Mk = sympy.eye(d)
    for k in range(d + 1):
        vecs.append(list(Mk))
        mat = sympy.Matrix(vecs)
        if mat.rank() < len(vecs):
            return k
        Mk = Mk * M
    return d

def conditions(witness):
    M = get_matrix(witness)
    
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    if M is not None:
        # H1: F is a field (entries of the matrix are in a field, e.g., Q)
        h1 = True
        # H2: alpha is an algebraic element over F (any square matrix is algebraic)
        h2 = True
        
        try:
            deg_alpha = minpoly_degree(M)
            # H3: the degree of the minimal polynomial of alpha over F is an odd integer
            h3 = (deg_alpha % 2 == 1)
        except Exception:
            h3 = False
            
        try:
            deg_alpha = minpoly_degree(M)
            deg_alpha2 = minpoly_degree(M**2)
            # neg_Q: The conclusion fails if the minimal polynomials have different degrees
            # (which also implies the algebras F(alpha) and F(alpha^2) are not equal)
            neg_q = (deg_alpha != deg_alpha2)
        except Exception:
            neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an algebraic element over F",
    "H_3: the degree of the minimal polynomial of alpha over F is an odd integer",
    "¬Q: the field extensions F(alpha) and F(alpha^2) are not equal, or the minimal polynomials have different degrees"
]

N_HYP = 3
NEG_Q_INDEX = 3