import sympy
from sympy import Matrix, eye, zeros

# Standard linear algebra objects that might be useful for constructing witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subset(basis1, basis2):
    """Check if span(basis1) is a subspace of span(basis2)."""
    if not basis1:
        return True
    if not basis2:
        return all(all(x == 0 for x in m[:]) for m in basis1)
    M1 = Matrix([m[:] for m in basis1])
    M2 = Matrix([m[:] for m in basis2])
    return M2.col_join(M1).rank() == M2.rank()

def product_bases(basis1, basis2):
    """Return a basis for the product space of two matrix spaces."""
    res = []
    for a in basis1:
        for b in basis2:
            res.append(a * b)
    return res

def intersect_bases(basis1, basis2):
    """Return a basis for the intersection of two matrix spaces."""
    if not basis1 or not basis2:
        return []
    shape = basis1[0].shape
    M1 = Matrix([m[:] for m in basis1]).T
    M2 = Matrix([m[:] for m in basis2]).T
    M = M1.row_join(-M2)
    ns = M.nullspace()
    res = []
    for v in ns:
        x = v[:M1.shape[1], :]
        vec = M1 * x
        res.append(Matrix(shape[0], shape[1], vec[:]))
    return res

def is_ring(R_basis):
    """Check if the span of R_basis is closed under matrix multiplication."""
    if not R_basis:
        return True
    prods = product_bases(R_basis, R_basis)
    return is_subset(prods, R_basis)

def is_ideal(I_basis, R_basis):
    """Check if the span of I_basis is a two-sided ideal of the span of R_basis."""
    if not is_subset(I_basis, R_basis):
        return False
    left_prods = product_bases(R_basis, I_basis)
    if not is_subset(left_prods, I_basis):
        return False
    right_prods = product_bases(I_basis, R_basis)
    if not is_subset(right_prods, I_basis):
        return False
    return True

def conditions(witness):
    """
    Check if the witness is a valid counterexample.
    The witness should be a tuple (R_basis, I_basis, J_basis) where each is a list
    of sympy.Matrix objects of the same square dimensions, representing bases for
    the ring R and its ideals I and J over a field.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        
        R_basis = list(witness[0])
        I_basis = list(witness[1])
        J_basis = list(witness[2])
        
        if not R_basis:
            return [False, False, False]
            
        if not isinstance(R_basis[0], Matrix):
            return [False, False, False]
            
        shape = R_basis[0].shape
        if shape[0] != shape[1]:
            return [False, False, False]
            
        for b in R_basis + I_basis + J_basis:
            if not isinstance(b, Matrix) or b.shape != shape:
                return [False, False, False]

        # H_1: I and J are ideals of R
        h1 = is_ring(R_basis) and is_ideal(I_basis, R_basis) and is_ideal(J_basis, R_basis)
        
        # H_2: I + J = R
        h2 = is_subset(R_basis, I_basis + J_basis) and is_subset(I_basis + J_basis, R_basis)
        
        # ¬Q: IJ != I \cap J
        IJ_basis = product_bases(I_basis, J_basis)
        I_cap_J_basis = intersect_bases(I_basis, J_basis)
        
        eq = is_subset(IJ_basis, I_cap_J_basis) and is_subset(I_cap_J_basis, IJ_basis)
        neg_q = not eq
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I + J = R",
    "¬Q: IJ != I \\cap J"
]

N_HYP = 2
NEG_Q_INDEX = 2