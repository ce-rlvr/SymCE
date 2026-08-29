import sympy as sp
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A and B are n x n complex matrices",
    "H_2: sigma_1(A) >= ... >= sigma_n(A) are the singular values of A",
    "¬Q: |Tr(AB)| > sum(sigma_i(A) * sigma_i(B)) for some enumeration of sigma(B)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    A, B = None, None
    sigma_A_given, sigma_B_given = None, None
    sv_A_eval = []

    # Unpack witness
    if isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            A, B = witness
        elif len(witness) == 3:
            A, B, sigma_A_given = witness
        elif len(witness) >= 4:
            A, B, sigma_A_given, sigma_B_given = witness[:4]
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    # Convert lists to sympy Matrices if necessary
    try:
        if isinstance(A, (list, tuple)):
            A = sp.Matrix(A)
        if isinstance(B, (list, tuple)):
            B = sp.Matrix(B)
    except Exception:
        pass

    # H_1: A and B are n x n complex matrices
    try:
        h1_ok = False
        if hasattr(A, 'is_Matrix') and A.is_Matrix and hasattr(B, 'is_Matrix') and B.is_Matrix:
            if A.rows == A.cols and B.rows == B.cols and A.rows == B.rows:
                h1_ok = True
    except Exception:
        h1_ok = False

    def get_singular_values(M):
        try:
            # Fast numerical SVD
            sv = M.evalf().singular_values()
            return [float(sp.re(sp.N(s))) for s in sv]
        except Exception:
            # Fallback to eigenvalues of M^H M
            M_H = M.H
            M_HM = M_H * M
            evals = list(M_HM.eigenvals(multiple=True))
            sv = []
            for e in evals:
                val = float(sp.re(sp.N(e)))
                if val < 0: 
                    val = 0
                sv.append(val**0.5)
            return sv

    # H_2: sigma_1(A) >= ... >= sigma_n(A) are the singular values of A
    try:
        h2_ok = False
        if h1_ok:
            sv_A_eval = get_singular_values(A)
            sv_A_eval.sort(reverse=True)
            h2_ok = True
            
            # If witness explicitly provides sigma_A, verify it matches and is sorted descending
            if sigma_A_given is not None:
                sig_A_eval = [float(sp.re(sp.N(s))) for s in sigma_A_given]
                if len(sv_A_eval) != len(sig_A_eval):
                    h2_ok = False
                else:
                    for s1, s2 in zip(sv_A_eval, sig_A_eval):
                        if abs(s1 - s2) > 1e-4:
                            h2_ok = False
                            break
                    for i in range(len(sig_A_eval) - 1):
                        if sig_A_eval[i] < sig_A_eval[i+1] - 1e-4:
                            h2_ok = False
                            break
    except Exception:
        h2_ok = False

    # ¬Q: The absolute value of the trace of A B is bounded above by sum(sigma_i(A) * sigma_i(B)) FAILS
    # Since the sorting of sigma(B) was dropped from the hypotheses, the bound fails if there is 
    # ANY enumeration of sigma(B) that violates it. We test the ascending order (which minimizes the sum).
    try:
        neg_q = False
        if h1_ok and h2_ok:
            sv_B_eval = get_singular_values(B)
            sv_B_eval.sort() # Ascending order to minimize the sum
            
            sv_B_to_use = sv_B_eval
            
            # If witness explicitly provides an enumeration for sigma_B, verify it's a valid permutation
            if sigma_B_given is not None:
                try:
                    sig_B_eval = [float(sp.re(sp.N(s))) for s in sigma_B_given]
                    if len(sig_B_eval) == len(sv_B_eval):
                        sorted_sig = sorted(sig_B_eval)
                        match = True
                        for s1, s2 in zip(sorted_sig, sv_B_eval):
                            if abs(s1 - s2) > 1e-4:
                                match = False
                                break
                        if match:
                            sv_B_to_use = sig_B_eval
                except Exception:
                    pass
            
            rhs = sum(a * b for a, b in zip(sv_A_eval, sv_B_to_use))
            
            AB = A * B
            tr = AB.trace()
            try:
                lhs = float(abs(sp.N(tr)))
            except Exception:
                lhs = float(abs(complex(tr)))
            
            if lhs > rhs + 1e-7:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]