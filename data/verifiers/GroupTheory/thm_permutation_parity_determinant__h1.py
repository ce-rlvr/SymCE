import sympy as sp
from sympy.combinatorics import Permutation
from sympy.matrices import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
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
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (sigma, P_sigma) where sigma is a permutation
    and P_sigma is its associated permutation matrix (potentially over a specific field/ring).
    """
    try:
        sigma, P_sigma = witness
    except Exception:
        return [False, False]
    
    def apply_sigma(sig, i):
        try:
            return sig(i)
        except IndexError:
            # SymPy permutations raise IndexError for elements >= size, acting as identity
            return i
        except Exception:
            return sig(i)

    # H_1: P_sigma is the n x n permutation matrix associated with sigma
    try:
        if hasattr(P_sigma, 'rows'):
            n = int(P_sigma.rows)
            cols = int(P_sigma.cols)
        else:
            n = len(P_sigma)
            cols = len(P_sigma[0]) if n > 0 else 0
            
        if cols != n:
            h1 = False
        else:
            is_perm = False
            # Check both standard conventions for permutation matrices
            for conv in [1, 2]:
                match = True
                for i in range(n):
                    for j in range(n):
                        if conv == 1:
                            expected = 1 if j == apply_sigma(sigma, i) else 0
                        else:
                            expected = 1 if i == apply_sigma(sigma, j) else 0
                        
                        try:
                            val = P_sigma[i, j]
                        except TypeError:
                            val = P_sigma[i][j]
                            
                        if expected == 1:
                            if val != 1:
                                match = False
                        else:
                            if val != 0:
                                match = False
                if match:
                    is_perm = True
                    break
            h1 = is_perm
    except Exception:
        h1 = False

    # neg_Q: The sign of the permutation sigma is NOT equal to the determinant of the matrix P_sigma
    try:
        sign = sigma.signature()
        
        if hasattr(P_sigma, 'det'):
            det = P_sigma.det()
        elif isinstance(P_sigma, list):
            det = Matrix(P_sigma).det()
        else:
            det = sp.det(P_sigma)
            
        neg_q = bool(sign != det)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P_sigma is the n x n permutation matrix associated with sigma",
    "¬Q: The sign of the permutation sigma is NOT equal to the determinant of the matrix P_sigma"
]

N_HYP = 1
NEG_Q_INDEX = 1