import sympy
from sympy import Matrix, eye, zeros, I
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            A, lam = witness
        else:
            A = witness
            lam = None
            
        if not isinstance(A, sympy.Matrix):
            A = sympy.Matrix(A)
            
        if lam is None:
            if hasattr(A, 'eigenvals'):
                for e in A.eigenvals():
                    re, im_part = e.as_real_imag()
                    im_part = sympy.simplify(im_part)
                    if im_part != 0:
                        lam = e
                        break
                        
        if not hasattr(A, 'shape') or len(A.shape) != 2 or A.shape[0] != A.shape[1]:
            return [False, False]
            
        n = A.shape[0]
        I_mat = sympy.eye(n)
        
        if lam is None:
            h1 = False
        else:
            re, im_part = lam.as_real_imag()
            im_part = sympy.simplify(im_part)
            if im_part == 0:
                h1 = False
            else:
                B = A - lam * I_mat
                h1 = B.rank() < n
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            re, im_part = lam.as_real_imag()
            clam = re - sympy.I * im_part
            
            def get_blocks(eig):
                N = [0]
                M = sympy.eye(n)
                B = A - eig * I_mat
                for m in range(1, n + 2):
                    M = M * B
                    N.append(n - M.rank())
                counts = {}
                for k in range(1, n + 1):
                    c = 2 * N[k] - N[k-1] - N[k+1]
                    if c > 0:
                        counts[k] = c
                return counts
            
            blocks_lam = get_blocks(lam)
            blocks_clam = get_blocks(clam)
            
            neg_q = (blocks_lam != blocks_clam)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: lambda is a complex eigenvalue of A with a non-zero imaginary part",
    "¬Q: The number of k x k Jordan blocks for lambda is not equal to the number for its conjugate"
]

N_HYP = 1
NEG_Q_INDEX = 1