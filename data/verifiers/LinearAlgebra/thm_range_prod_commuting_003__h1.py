import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        P, Q = witness
    except Exception:
        return [False, False]
        
    try:
        if not (hasattr(P, 'row_join') and hasattr(Q, 'row_join')):
            h1 = False
        elif P.rows != P.cols or Q.rows != Q.cols or P.rows != Q.rows:
            h1 = False
        else:
            h1 = bool(P * Q == Q * P)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n_rows = P.rows
            PQ = P * Q
            
            # To find Col(P) ∩ Col(Q), we solve [P, -Q] * [x; y] = 0
            M_concat = P.row_join(-Q)
            null_basis = M_concat.nullspace()
            
            vecs_intersect = []
            for n in null_basis:
                # Extract the 'x' part of the nullspace vector
                x_vec = n[:P.cols, :]
                # The vector in the intersection is P * x
                v = P * x_vec
                vecs_intersect.append(v)
                
            M1 = PQ
            if vecs_intersect:
                M2 = vecs_intersect[0]
                for vec in vecs_intersect[1:]:
                    M2 = M2.row_join(vec)
            else:
                M2 = zeros(n_rows, 1)
                
            r1 = M1.rank()
            r2 = M2.rank()
            r12 = M1.row_join(M2).rank()
            
            spans_equal = (r1 == r2) and (r2 == r12)
            neg_q = not spans_equal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P and Q commute (PQ = QP)",
    "¬Q: Col(PQ) is not equal to Col(P) ∩ Col(Q)"
]

N_HYP = 1
NEG_Q_INDEX = 1