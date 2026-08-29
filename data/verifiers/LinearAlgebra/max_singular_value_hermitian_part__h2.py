import sympy as sp
import math

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "H_2: sigma_1(.) denotes the maximum singular value of a matrix",
    "¬Q: sigma_1(H) > sigma_1(A)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Since the hypothesis "H is the Hermitian part of A" was dropped,
        # H is a free variable and must be provided in the witness.
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, H = witness
        else:
            A = witness
            H = None
    except Exception:
        A = witness
        H = None

    # H_1: A is an n x n complex matrix
    h1_ok = False
    try:
        A_mat = sp.Matrix(A)
        if A_mat.rows == A_mat.cols and A_mat.rows > 0:
            h1_ok = True
    except Exception:
        pass

    # H_2: sigma_1(.) denotes the maximum singular value of a matrix
    # This is a definitional hypothesis, so it evaluates to True.
    h2_ok = True

    # neg_Q: sigma_1(H) > sigma_1(A)
    neg_q_ok = False
    try:
        if h1_ok and H is not None:
            H_mat = sp.Matrix(H)
            if H_mat.rows == H_mat.cols and H_mat.rows > 0:
                def max_sv(M):
                    try:
                        # Compute eigenvalues of M^H * M
                        M_H_M = M.H * M
                        evs = M_H_M.eigenvals()
                        max_ev = 0
                        for ev in evs.keys():
                            val = float(sp.re(sp.N(ev)))
                            if val > max_ev:
                                max_ev = val
                        return math.sqrt(max_ev)
                    except Exception:
                        return None
                
                s_A = max_sv(A_mat)
                s_H = max_sv(H_mat)
                
                if s_A is not None and s_H is not None:
                    if s_H > s_A + 1e-9:
                        neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]