import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        # Witness can be a tuple (A, lambda) or just a matrix A
        if isinstance(witness, tuple):
            if len(witness) == 2:
                A, lam = witness
            else:
                return [False, False]
        else:
            A = witness
            lam = None
            
        if not isinstance(A, Matrix):
            return [False, False]
            
        # H_1: A is a square matrix over the complex numbers
        h1 = A.is_square
        if h1:
            for val in A:
                if not (val.is_complex or val.has(sympy.Symbol)):
                    h1 = False
                    break
                    
        def check_lam(mat, eigenvalue):
            # Calculate geometric multiplicity
            eigenvects = mat.eigenvects()
            geom_mult = 0
            for ev, alg, vecs in eigenvects:
                if ev == eigenvalue:
                    geom_mult = len(vecs)
                    break
            
            # Calculate number of Jordan blocks for the eigenvalue
            P, J = mat.jordan_form()
            num_blocks = 0
            n = J.shape[0]
            for i in range(n):
                if J[i, i] == eigenvalue:
                    # A new Jordan block starts if it's the first element or the superdiagonal element above it is 0
                    if i == 0 or J[i-1, i] == 0:
                        num_blocks += 1
                        
            return num_blocks == geom_mult

        # Evaluate conclusion
        if lam is not None:
            q = check_lam(A, lam)
        else:
            # If lambda is not specified, the property should hold for all eigenvalues
            q = True
            for ev, alg, vecs in A.eigenvects():
                if not check_lam(A, ev):
                    q = False
                    break
                    
        neg_q = not q
        return [bool(h1), bool(neg_q)]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: A is a square matrix over the complex numbers",
    "¬Q: The number of Jordan blocks corresponding to lambda in the Jordan canonical form of A is not exactly the geometric multiplicity of lambda"
]

N_HYP = 1
NEG_Q_INDEX = 1