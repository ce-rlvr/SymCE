import sympy
from sympy import Matrix, eye, zeros
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_spectral_norm_exact(M):
    sv = M.singular_values()
    if not sv:
        return sympy.S.Zero
    try:
        return max(sv)
    except Exception:
        # Fallback to numerical comparison if symbolic max fails
        max_val = sv[0]
        max_float = float(sv[0].evalf())
        for s in sv[1:]:
            s_float = float(s.evalf())
            if s_float > max_float:
                max_float = s_float
                max_val = s
        return max_val

def conditions(witness):
    A = witness.get('A')
    U = witness.get('U')
    Sigma = witness.get('Sigma')
    V = witness.get('V')
    k = witness.get('k')
    A_k = witness.get('A_k')
    B = witness.get('B')

    # H_1: A = U Σ V^* is the SVD of A with singular values σ_1 ≥ ... ≥ σ_r > 0
    h1 = False
    sigmas = []
    r = 0
    try:
        if all(x is not None for x in [A, U, Sigma, V]):
            if sympy.simplify(A - U * Sigma * V.H) == sympy.zeros(A.rows, A.cols):
                if sympy.simplify(U.H * U - sympy.eye(U.cols)) == sympy.zeros(U.cols, U.cols):
                    if sympy.simplify(V.H * V - sympy.eye(V.cols)) == sympy.zeros(V.cols, V.cols):
                        is_diag = True
                        for i in range(Sigma.rows):
                            for j in range(Sigma.cols):
                                if i != j and Sigma[i, j] != 0:
                                    is_diag = False
                                    break
                            if not is_diag:
                                break
                        if is_diag:
                            for i in range(min(Sigma.rows, Sigma.cols)):
                                sigmas.append(Sigma[i, i])
                            for s in sigmas:
                                is_pos = False
                                try:
                                    is_pos = bool(s > 0)
                                except TypeError:
                                    is_pos = s.is_positive
                                if is_pos:
                                    r += 1
                                else:
                                    break
                            if r > 0:
                                h1 = True
                                for i in range(r - 1):
                                    try:
                                        if bool(sigmas[i] < sigmas[i+1]):
                                            h1 = False
                                            break
                                    except TypeError:
                                        if sympy.simplify(sigmas[i+1] - sigmas[i]).is_positive:
                                            h1 = False
                                            break
                                for i in range(r, len(sigmas)):
                                    if sympy.simplify(sigmas[i]) != 0:
                                        h1 = False
                                        break
    except Exception:
        h1 = False

    # H_2: k is an integer such that 1 ≤ k < r
    h2 = False
    try:
        if h1 and isinstance(k, int) and 1 <= k < r:
            h2 = True
    except Exception:
        h2 = False

    # H_3: A_k = ∑_{i=1}^k σ_i u_i v_i^* is the truncated SVD of A
    h3 = False
    try:
        if h1 and h2 and A_k is not None:
            expected_A_k = sympy.zeros(U.rows, V.rows)
            for i in range(k):
                u_i = U[:, i]
                v_i = V[:, i]
                sigma_i = Sigma[i, i]
                expected_A_k += sigma_i * u_i * v_i.H
            if sympy.simplify(A_k - expected_A_k) == sympy.zeros(A_k.rows, A_k.cols):
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: A_k does not minimize the spectral norm or the minimum error is not exactly σ_{k+1}
    neg_q = False
    try:
        if h1 and h2 and h3:
            sigma_k_plus_1 = sigmas[k]
            err_A_k = get_spectral_norm_exact(A - A_k)
            
            # Check if the error is exactly σ_{k+1}
            diff_exact = sympy.simplify(err_A_k - sigma_k_plus_1)
            if diff_exact != 0:
                try:
                    if abs(float(diff_exact.evalf())) > 1e-7:
                        neg_q = True
                except Exception:
                    neg_q = True
            
            # Check if a better approximation B of rank <= k exists
            if not neg_q and B is not None:
                if B.rank() <= k:
                    err_B = get_spectral_norm_exact(A - B)
                    diff_err = sympy.simplify(err_A_k - err_B)
                    try:
                        if diff_err.is_positive:
                            neg_q = True
                        elif diff_err != 0 and float(diff_err.evalf()) > 1e-7:
                            neg_q = True
                    except Exception:
                        try:
                            if float(diff_err.evalf()) > 1e-7:
                                neg_q = True
                        except Exception:
                            pass
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A = U Σ V^* is the SVD of A with singular values σ_1 ≥ ... ≥ σ_r > 0",
    "H_2: k is an integer such that 1 ≤ k < r",
    "H_3: A_k is the truncated SVD of A",
    "¬Q: A_k does not minimize the spectral norm or the minimum error is not exactly σ_{k+1}"
]

N_HYP = 3
NEG_Q_INDEX = 3