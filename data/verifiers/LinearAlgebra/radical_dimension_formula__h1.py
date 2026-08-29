import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: B is a symmetric bilinear form on V (M is symmetric)",
    "H_2: M is the Gram matrix of B relative to some basis of V (M is square)",
    "¬Q: The dimension of V does not equal the rank of M plus the dimension of the radical of B"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        # Allow witness to be a tuple (M, rank_M, dim_rad_B) to support matrices over rings
        # where sympy's default rank() and nullspace() over Q might not apply.
        if isinstance(witness, tuple):
            if len(witness) == 3:
                M, rank_M, dim_rad_B = witness
            elif len(witness) == 2:
                M, dim_rad_B = witness
                if callable(M.rank):
                    rank_M = M.rank()
                else:
                    rank_M = M.rank
            else:
                M = witness[0]
                if callable(M.rank):
                    rank_M = M.rank()
                else:
                    rank_M = M.rank
                if callable(M.nullspace):
                    ns = M.nullspace()
                else:
                    ns = M.nullspace
                dim_rad_B = len(ns)
        else:
            M = witness
            if callable(M.rank):
                rank_M = M.rank()
            else:
                rank_M = M.rank
            if callable(M.nullspace):
                ns = M.nullspace()
            else:
                ns = M.nullspace
            dim_rad_B = len(ns)
            
        # H_1: B is a symmetric bilinear form on V.
        # This implies its Gram matrix M is symmetric.
        if callable(M.is_symmetric):
            h1 = bool(M.is_symmetric())
        else:
            h1 = bool(M.is_symmetric)
            
        # H_2: M is the Gram matrix of B relative to some basis of V.
        # This implies M must be a square matrix.
        if callable(M.is_square):
            h2 = bool(M.is_square())
        else:
            h2 = bool(M.is_square)
            
        # The dimension of V is the size of the Gram matrix M.
        dim_V = M.shape[0]
        
        # ¬Q: The dimension of V does NOT equal the rank of M plus the dimension of the radical of B.
        neg_q = (dim_V != rank_M + dim_rad_B)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]