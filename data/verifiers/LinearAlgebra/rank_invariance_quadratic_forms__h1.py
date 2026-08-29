import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            A, B, P = witness
            A = sympy.Matrix(A)
            B = sympy.Matrix(B)
            P = sympy.Matrix(P)
        elif len(witness) == 2:
            A, B = witness
            A = sympy.Matrix(A)
            B = sympy.Matrix(B)
            P = -sympy.eye(A.shape[0])
        else:
            return [False, False]
            
        if A.shape != B.shape or A.shape != P.shape or A.shape[0] != A.shape[1]:
            return [False, False]
            
        n = A.shape[0]
        
        P_inv_exists = P.det() != 0
        different_bases = P != sympy.eye(n)
        same_qf = (B + B.T) == P.T * (A + A.T) * P
        
        h1 = bool(P_inv_exists and different_bases and same_qf)
        neg_q = bool(A.rank() != B.rank())
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: A and B are matrix representations of Q with respect to two different bases of V",
    "¬Q: The rank of matrix A is not equal to the rank of matrix B"
]

N_HYP = 1
NEG_Q_INDEX = 1