import sympy as sp
from sympy.matrices import Matrix, eye, zeros, MatrixBase
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: T is a linear transformation",
    "H_2: T^* is the dual map of T",
    "¬Q: ker(T^*) != (im(T))^0"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # H1: T is a linear transformation
        # We represent the linear transformation T as a matrix.
        if isinstance(witness, list):
            try:
                A = Matrix(witness)
            except Exception:
                return [False, False, False]
        elif isinstance(witness, MatrixBase):
            A = witness
        else:
            return [False, False, False]
            
        h1 = True
        
        # H2: T^* is the dual map of T
        # This is a definitional hypothesis, inherently true for our setup.
        h2 = True
        
        # Conclusion: ker(T^*) = (im(T))^0
        # ker(T^*) is the nullspace of the transpose matrix A.T
        ker_T_star = A.T.nullspace()
        
        # im(T) is the column space of A
        im_T = A.columnspace()
        
        if not im_T:
            # If the image is the zero subspace, its annihilator is the entire dual space
            im_T_annihilator = eye(A.shape[0]).columnspace()
        else:
            # The annihilator of im(T) consists of all linear functionals (row vectors)
            # that vanish on the column space. This is the left nullspace of the basis matrix.
            im_T_matrix = Matrix.hstack(*im_T)
            im_T_annihilator = im_T_matrix.T.nullspace()
            
        def span_eq(span1, span2):
            if len(span1) != len(span2):
                return False
            if len(span1) == 0:
                return True
            M1 = Matrix.hstack(*span1)
            M2 = Matrix.hstack(*span2)
            M_both = Matrix.hstack(M1, M2)
            return M1.rank() == M_both.rank()
            
        q = span_eq(ker_T_star, im_T_annihilator)
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]