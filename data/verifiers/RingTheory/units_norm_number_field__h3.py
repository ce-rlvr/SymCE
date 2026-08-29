import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_matrix(minpoly_expr, alpha_expr):
    """
    Computes the matrix of the multiplication by alpha map in the field K = Q[x]/(minpoly).
    The basis used is 1, x, x^2, ..., x^{d-1}.
    """
    minpoly = sp.Poly(minpoly_expr, x, domain='QQ')
    alpha = sp.Poly(alpha_expr, x, domain='QQ')
    d = minpoly.degree()
    if d < 1:
        raise ValueError("Degree must be >= 1")
    
    M = sp.zeros(d, d)
    for i in range(d):
        term = sp.Poly(x**i, x, domain='QQ')
        prod = (alpha * term) % minpoly
        coeffs = prod.all_coeffs()
        # all_coeffs returns coefficients from highest degree to lowest
        coeffs = [0]*(d - len(coeffs)) + coeffs
        for j in range(d):
            # Place the coefficient of x^{d - 1 - j} in the correct row
            M[d - 1 - j, i] = coeffs[j]
    return M

def conditions(witness):
    """
    witness: A tuple (minpoly_expr, alpha_expr)
    - minpoly_expr: The minimal polynomial of a primitive element of K over Q (in variable x).
    - alpha_expr: A polynomial in x representing the element alpha in K.
    """
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        minpoly_expr, alpha_expr = witness
    except Exception:
        return [False, False, False, False]

    # H1: K is an algebraic number field
    try:
        minpoly = sp.Poly(minpoly_expr, x, domain='QQ')
        h1 = (minpoly.degree() >= 1) and (minpoly.LC() == 1) and minpoly.is_irreducible
    except Exception:
        h1 = False

    # H2: O_K is the ring of integers of K
    # This is a definitional binding for the field K.
    h2 = True if h1 else False

    # H3: alpha is an element of O_K
    try:
        M = get_matrix(minpoly_expr, alpha_expr)
        cp = M.charpoly()
        h3 = True
        for c in cp.coeffs():
            if not sp.sympify(c).is_Integer:
                h3 = False
                break
    except Exception:
        h3 = False

    # neg_Q: alpha is a unit in O_K iff N_{K/Q}(alpha) = 1 or N_{K/Q}(alpha) = -1
    try:
        M = get_matrix(minpoly_expr, alpha_expr)
        norm = M.det()
        norm_cond = (norm == 1 or norm == -1)
        
        if norm == 0:
            is_unit = False
        else:
            M_inv = M.inv()
            cp_inv = M_inv.charpoly()
            is_unit = True
            for c in cp_inv.coeffs():
                if not sp.sympify(c).is_Integer:
                    is_unit = False
                    break
        
        # The conclusion is: is_unit == norm_cond
        # We return True if the conclusion FAILS
        neg_q = (is_unit != norm_cond)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraic number field",
    "H_2: O_K is the ring of integers of K",
    "H_3: alpha is an element of O_K",
    "¬Q: It is not the case that (alpha is a unit in O_K iff N_{K/Q}(alpha) = 1 or -1)"
]

N_HYP = 3
NEG_Q_INDEX = 3