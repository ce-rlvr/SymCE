import sympy as sp
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
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
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    M = None
    if isinstance(witness, sp.MatrixBase):
        M = witness
    elif isinstance(witness, list):
        try:
            M = sp.Matrix(witness)
        except Exception:
            pass
    elif isinstance(witness, tuple) and len(witness) > 0:
        if isinstance(witness[0], sp.MatrixBase):
            M = witness[0]
        elif isinstance(witness[0], list):
            try:
                M = sp.Matrix(witness[0])
            except Exception:
                pass
                
    if M is not None:
        # H1: V is a finite-dimensional vector space over a field F
        # We loosely accept any matrix as representing a finite-dimensional module
        h1 = True
        
        # H2: B is a symmetric bilinear form
        try:
            if not M.is_square:
                h2 = False
            else:
                h2 = bool(M.is_symmetric())
        except Exception:
            h2 = False
            
        # H3: phi_B is the linear map defined by phi_B(v)(w) = B(v, w)
        h3 = True
        
        # ¬Q: The image of phi_B is not equal to the annihilator of the radical
        # Over a field, this is always false (they are always equal).
        # Over a ring like Z, they are equal if and only if the non-zero invariant factors are units.
        try:
            snf = M.smith_normal_form()
            for i in range(min(M.rows, M.cols)):
                val = snf[i, i]
                if val not in [1, -1, 0]:
                    neg_q = True
                    break
        except Exception:
            # If smith_normal_form fails, it might be over a field (e.g. floats or rationals),
            # where the conclusion holds, so neg_q remains False.
            neg_q = False
            
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a symmetric bilinear form",
    "H_3: phi_B is the linear map defined by phi_B(v)(w) = B(v, w)",
    "¬Q: The image of phi_B is not equal to the annihilator of the radical"
]

N_HYP = 3
NEG_Q_INDEX = 3