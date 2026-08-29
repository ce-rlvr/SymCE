import sympy
from sympy import Matrix

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

# Standard 2x2 matrix basis units
E11 = Matrix([[1, 0], [0, 0]])
E12 = Matrix([[0, 1], [0, 0]])
E21 = Matrix([[0, 0], [1, 0]])
E22 = Matrix([[0, 0], [0, 1]])

def basis(A):
    """Returns a basis for the vector space spanned by a list of matrices."""
    if not A:
        return []
    shape = A[0].shape
    # Flatten each matrix into a row vector
    M = Matrix([list(a) for a in A])
    rref_M, _ = M.rref()
    res = []
    for i in range(rref_M.shape[0]):
        row = rref_M.row(i)
        if not all(x == 0 for x in row):
            res.append(Matrix(shape[0], shape[1], list(row)))
    return res

def mul_spaces(A, B):
    """Returns a basis for the space spanned by all products a * b."""
    if not A or not B:
        return []
    prods = [a * b for a in A for b in B]
    return basis(prods)

def is_subspace(A, B):
    """Checks if space A is a subspace of space B."""
    return len(basis(A + B)) == len(basis(B))

def equal_spaces(A, B):
    """Checks if space A and space B are the same."""
    return is_subspace(A, B) and is_subspace(B, A)

def is_ideal(I, R):
    """Checks if I is a two-sided ideal of R."""
    if not is_subspace(I, R):
        return False
    if not is_subspace(mul_spaces(R, I), I):
        return False
    if not is_subspace(mul_spaces(I, R), I):
        return False
    return True

def power_space(A, n):
    """Computes the n-th power of an ideal/space A."""
    if n <= 0:
        return []
    if n == 1:
        return basis(A)
    res = basis(A)
    for _ in range(n - 1):
        res = mul_spaces(res, A)
    return res

def conditions(witness):
    """
    Expects witness to be a tuple: (R, I, J, n)
    where R, I, J are lists of sympy.Matrix representing bases of the ring and ideals,
    and n is an integer.
    """
    try:
        R, I, J, n = witness
    except Exception:
        return [False, False, False]

    # H_1: I and J are ideals of R
    try:
        # R must be closed under multiplication to be a valid ring
        R_is_ring = is_subspace(mul_spaces(R, R), R)
        h1 = R_is_ring and is_ideal(I, R) and is_ideal(J, R)
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h2 = False

    # ¬Q: (IJ)^n != I^n J^n
    try:
        IJ = mul_spaces(I, J)
        IJ_n = power_space(IJ, n)
        
        I_n = power_space(I, n)
        J_n = power_space(J, n)
        In_Jn = mul_spaces(I_n, J_n)
        
        neg_q = not equal_spaces(IJ_n, In_Jn)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: n is a positive integer",
    "¬Q: (IJ)^n != I^n J^n"
]

N_HYP = 2
NEG_Q_INDEX = 2