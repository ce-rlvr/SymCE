import sympy as sp
from sympy.matrices import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            h1 = False
        else:
            A, E = witness
            h1 = isinstance(A, sp.MatrixBase) and isinstance(E, sp.MatrixBase)
    except Exception:
        h1 = False

    try:
        if not h1:
            return [False, False]
        
        A, E = witness
        m, n = A.shape
        
        Q = True
        try:
            if A.shape != E.shape:
                Q = False
            else:
                A_plus_E = A + E
                
                sv_A = A.singular_values()
                sv_E = E.singular_values()
                sv_A_plus_E = A_plus_E.singular_values()
                
                sv_A = sorted([float(sp.re(val.evalf())) for val in sv_A], reverse=True)
                sv_E = sorted([float(sp.re(val.evalf())) for val in sv_E], reverse=True)
                sv_A_plus_E = sorted([float(sp.re(val.evalf())) for val in sv_A_plus_E], reverse=True)
                
                limit = min(m, n)
                while len(sv_A) < limit: 
                    sv_A.append(0.0)
                while len(sv_A_plus_E) < limit: 
                    sv_A_plus_E.append(0.0)
                
                sigma_1_E = sv_E[0] if len(sv_E) > 0 else 0.0
                
                for i in range(limit):
                    diff = abs(sv_A_plus_E[i] - sv_A[i])
                    if diff > sigma_1_E + 1e-7:
                        Q = False
                        break
        except Exception:
            # If computation fails for a reason other than ShapeError (e.g. symbolic matrix),
            # we assume Q is True to avoid false positives, as Weyl's inequality holds for all
            # matrices of the same dimensions.
            Q = True
            
        neg_Q = not Q
        
    except Exception:
        neg_Q = False

    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: Let sigma_i(M) denote the i-th largest singular value of a matrix M",
    "¬Q: The inequality |sigma_i(A+E) - sigma_i(A)| <= sigma_1(E) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1