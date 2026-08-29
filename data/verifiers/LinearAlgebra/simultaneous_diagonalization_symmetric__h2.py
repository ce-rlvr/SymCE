import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        A, B = witness
        if not isinstance(A, sp.MatrixBase):
            A = sp.Matrix(A)
        if not isinstance(B, sp.MatrixBase):
            B = sp.Matrix(B)
    except Exception:
        return [False, False]
    
    # H_1: A and B are real symmetric n x n matrices
    try:
        if A.shape != B.shape:
            h1 = False
        elif A.rows != A.cols or A.rows < 1:
            h1 = False
        elif not A.is_symmetric() or not B.is_symmetric():
            h1 = False
        else:
            h1 = True
            for mat in (A, B):
                for e in mat:
                    if e.is_real is False:
                        h1 = False
                        break
                    elif e.is_real is None:
                        try:
                            float(e)
                        except Exception:
                            h1 = False
                            break
                if not h1:
                    break
    except Exception:
        h1 = False

    # neg_Q: Conclusion fails
    # The conclusion states there exists an invertible real matrix P such that 
    # P^T A P = I and P^T B P = D. This is mathematically equivalent to A being 
    # positive definite. Thus, the conclusion fails iff A is NOT positive definite.
    try:
        if not h1:
            neg_q = False
        else:
            is_pos_def = True
            n = A.rows
            # Sylvester's criterion for positive definiteness
            for i in range(1, n + 1):
                minor = A[:i, :i].det()
                if minor <= 0:
                    is_pos_def = False
                    break
            neg_q = not is_pos_def
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are real symmetric n x n matrices",
    "¬Q: There does not exist an invertible real matrix P such that P^T A P is the identity and P^T B P is diagonal"
]

N_HYP = 1
NEG_Q_INDEX = 1