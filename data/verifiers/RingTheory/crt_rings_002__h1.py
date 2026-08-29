import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_subspace(matrices, shape):
    if not matrices:
        return []
    M = sympy.Matrix([list(m) for m in matrices])
    rref_M, _ = M.rref()
    basis = []
    for i in range(rref_M.rows):
        row = list(rref_M.row(i))
        if any(x != 0 for x in row):
            basis.append(sympy.Matrix(shape[0], shape[1], row))
    return basis

def in_subspace(A, basis):
    if not basis:
        return all(x == 0 for x in A)
    M = sympy.Matrix([list(m) for m in basis] + [list(A)])
    return M.rank() == len(basis)

def is_subset(basis1, basis2):
    if not basis1: return True
    if not basis2: return False
    M2 = sympy.Matrix([list(m) for m in basis2])
    rank2 = M2.rank()
    for m in basis1:
        M = sympy.Matrix([list(x) for x in basis2] + [list(m)])
        if M.rank() > rank2:
            return False
    return True

def subspaces_equal(basis1, basis2):
    return is_subset(basis1, basis2) and is_subset(basis2, basis1)

def intersect_subspaces(basis1, basis2, shape):
    if not basis1 or not basis2:
        return []
    M1 = sympy.Matrix([list(m) for m in basis1])
    M2 = sympy.Matrix([list(m) for m in basis2])
    M = M1.col_join(M2)
    null_space = M.T.nullspace()
    intersection_basis = []
    for vec in null_space:
        x = vec[:len(basis1), 0]
        v_flat = (x.T * M1).row(0)
        if any(val != 0 for val in v_flat):
            intersection_basis.append(sympy.Matrix(shape[0], shape[1], list(v_flat)))
    return get_subspace(intersection_basis, shape)

def product_ideal(basis1, basis2, shape):
    prods = []
    for m1 in basis1:
        for m2 in basis2:
            prods.append(m1 * m2)
    return get_subspace(prods, shape)

def is_ring(R_basis, shape):
    for r1 in R_basis:
        for r2 in R_basis:
            if not in_subspace(r1 * r2, R_basis):
                return False
    return True

def is_ideal(I_basis, R_basis, shape):
    if not is_subset(I_basis, R_basis):
        return False
    for r in R_basis:
        for x in I_basis:
            if not in_subspace(r * x, I_basis):
                return False
            if not in_subspace(x * r, I_basis):
                return False
    return True

def conditions(witness):
    """
    witness: A tuple (R_basis, I_basis, J_basis) where each is a list of matrices 
             (or lists of lists) representing the basis of the ring R and ideals I, J.
    """
    try:
        R_raw, I_raw, J_raw = witness
        
        # Convert to sympy Matrices
        R_basis = [sympy.Matrix(m) for m in R_raw]
        I_basis = [sympy.Matrix(m) for m in I_raw]
        J_basis = [sympy.Matrix(m) for m in J_raw]
        
        # Determine matrix shape
        shape = None
        for b in [R_basis, I_basis, J_basis]:
            if b:
                shape = b[0].shape
                break
        if shape is None:
            # Trivial ring R=0, I=0, J=0. Conclusion holds (0 = 0), so not a counterexample.
            return [True, True, False]
            
        # Get linearly independent bases
        R_basis = get_subspace(R_basis, shape)
        I_basis = get_subspace(I_basis, shape)
        J_basis = get_subspace(J_basis, shape)
        
        # H_1: I and J are ideals of R
        h1 = is_ring(R_basis, shape) and is_ideal(I_basis, R_basis, shape) and is_ideal(J_basis, R_basis, shape)
        
        # H_2: I + J = R
        I_plus_J = get_subspace(I_basis + J_basis, shape)
        h2 = subspaces_equal(I_plus_J, R_basis)
        
        # ¬Q: I \cap J \neq IJ
        I_cap_J = intersect_subspaces(I_basis, J_basis, shape)
        IJ = product_ideal(I_basis, J_basis, shape)
        neg_q = not subspaces_equal(I_cap_J, IJ)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I + J = R",
    "¬Q: I \\cap J \\neq IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2