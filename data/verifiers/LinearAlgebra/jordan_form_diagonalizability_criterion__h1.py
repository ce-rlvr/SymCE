import sympy as sp
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
        A, J = witness
    except Exception:
        return [False, False]
        
    try:
        # H_1: J is the Jordan canonical form of A
        P, J_actual = A.jordan_form()
        h1 = bool(J == J_actual)
    except Exception:
        h1 = False
        
    try:
        # Conclusion: A is diagonalizable if and only if J is a diagonal matrix.
        # In the context of this false conjecture, "diagonalizable" for a real matrix 
        # implies diagonalizable over the Reals. The Jordan form, however, is computed 
        # over the algebraic closure (Complex numbers).
        is_real = True
        for x in A:
            if getattr(x, 'is_real', None) is not True:
                is_real = False
                break
                
        if is_real:
            is_diag = A.is_diagonalizable(reals_only=True)
        else:
            is_diag = A.is_diagonalizable()
            
        j_is_diag = J.is_diagonal()
        
        # The conclusion is (is_diag == j_is_diag).
        # We want the negation of the conclusion.
        neg_q = not (is_diag == j_is_diag)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: J is the Jordan canonical form of A",
    "¬Q: It is not the case that A is diagonalizable if and only if J is a diagonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1