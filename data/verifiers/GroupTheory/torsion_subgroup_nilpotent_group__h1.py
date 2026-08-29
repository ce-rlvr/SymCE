import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory and linear algebra objects
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

def conditions(witness):
    try:
        # The witness should be a tuple of two matrices (A, B) that generate the group G.
        # A and B must have finite order, but A*B must have infinite order.
        matrix_A, matrix_B = witness
        
        if not isinstance(matrix_A, Matrix) or not isinstance(matrix_B, Matrix):
            return [False, False]
            
        if matrix_A.shape != matrix_B.shape or matrix_A.shape[0] != matrix_A.shape[1]:
            return [False, False]
            
        n = matrix_A.shape[0]
        # Restrict dimension to ensure maximum finite order of integer matrices is well below 100
        if n > 5:
            return [False, False]
            
        if not all(x.is_integer == True for x in matrix_A) or not all(x.is_integer == True for x in matrix_B):
            return [False, False]
            
        # H1: T is the subset of G consisting of all elements of finite order.
        # This is a definitional hypothesis. We just check that A and B are valid group elements (invertible).
        h1 = (matrix_A.det() != 0) and (matrix_B.det() != 0)
        
        def is_finite_order(M):
            I = eye(n)
            Mk = I
            for k in range(1, 101):
                Mk = Mk * M
                if Mk == I:
                    return True
            return False
            
        # neg_Q: T is not a normal subgroup of G.
        # If A and B have finite order, they are in T.
        # If A*B has infinite order, it is not in T.
        # Thus T is not closed under multiplication, so T is not a subgroup.
        neg_q = is_finite_order(matrix_A) and is_finite_order(matrix_B) and not is_finite_order(matrix_A * matrix_B)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: T is the subset of G consisting of all elements of finite order",
    "¬Q: T is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1