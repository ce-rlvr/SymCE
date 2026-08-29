import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is an m x n real matrix of rank n with m >= n",
    "¬Q: QQ^T is not the orthogonal projection operator onto the column space of A"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The witness must provide both A and Q, since Q is not defined in the remaining hypotheses.
        if isinstance(witness, dict):
            A = witness.get('A')
            Q = witness.get('Q')
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            A = witness[0]
            Q = witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        if isinstance(A, sp.MatrixBase):
            m, n = A.shape
            if m >= n and A.rank() == n:
                if all(e.is_real for e in A):
                    h1_ok = True
    except Exception:
        pass

    neg_q_ok = False
    try:
        if isinstance(A, sp.MatrixBase) and isinstance(Q, sp.MatrixBase):
            AtA = A.T * A
            # A has full column rank, so A^T A should be invertible
            if AtA.det() != 0:
                # Orthogonal projection matrix onto the column space of A
                P = A * AtA.inv() * A.T
                QQt = Q * Q.T
                
                if P.shape == QQt.shape:
                    diff = P - QQt
                    if not diff.is_zero_matrix:
                        is_zero = True
                        for val in diff:
                            val_simp = sp.simplify(val)
                            if val_simp == 0:
                                continue
                            try:
                                # Account for potential floating-point inaccuracies
                                if abs(float(val_simp)) > 1e-10:
                                    is_zero = False
                                    break
                            except TypeError:
                                # If it cannot be cast to float (e.g., symbolic or complex), it's non-zero
                                is_zero = False
                                break
                        if not is_zero:
                            neg_q_ok = True
                else:
                    # If shapes do not match, it cannot be the projection operator
                    neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]