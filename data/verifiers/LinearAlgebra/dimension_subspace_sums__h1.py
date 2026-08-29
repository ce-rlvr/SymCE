import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def to_matrix(obj):
    if isinstance(obj, Matrix):
        return obj
    if isinstance(obj, (list, tuple)):
        obj = list(obj)
        if len(obj) > 0 and not isinstance(obj[0], (list, tuple)):
            return Matrix([obj])
        return Matrix(obj)
    return Matrix(obj)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        
        U_input, W_input = witness
        U_mat = to_matrix(U_input)
        W_mat = to_matrix(W_input)
        
        # Determine if the inputs are row vectors or column vectors
        if U_mat.cols == W_mat.cols:
            # Treat as row vectors (standard for list of lists)
            pass
        elif U_mat.rows == W_mat.rows:
            # Treat as column vectors, transpose to work with row spaces
            U_mat = U_mat.T
            W_mat = W_mat.T
        else:
            # Dimensions do not match, cannot be subspaces of the same vector space V
            return [False, False]
            
        # H_1: U and W are finite-dimensional subspaces of V
        # Represented by finite matrices, they are valid finite-dimensional subspaces.
        h1 = True
        
        # Compute dimensions
        dim_U = U_mat.rank()
        dim_W = W_mat.rank()
        
        # Dimension of U + W
        U_plus_W = U_mat.col_join(W_mat)
        dim_U_plus_W = U_plus_W.rank()
        
        # Dimension of U \cap W
        A = U_mat.T
        B = W_mat.T
        M = A.row_join(-B)
        null_basis = M.nullspace()
        
        if not null_basis:
            dim_U_cap_W = 0
        else:
            intersection_vectors = []
            for vec in null_basis:
                # Extract the coefficients corresponding to A
                x = vec[:A.cols, 0]
                v = A * x
                intersection_vectors.append(v)
            I_mat = Matrix.hstack(*intersection_vectors)
            dim_U_cap_W = I_mat.rank()
            
        # Conclusion: dim(U + W) = dim(U) + dim(W) - dim(U \cap W)
        conclusion = (dim_U_plus_W == dim_U + dim_W - dim_U_cap_W)
        neg_q = not conclusion
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: U and W are finite-dimensional subspaces of V",
    "¬Q: dim(U + W) != dim(U) + dim(W) - dim(U \\cap W)"
]
N_HYP = 1
NEG_Q_INDEX = 1