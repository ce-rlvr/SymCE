import sympy as sp
import math

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            lambda_val = witness.get('lambda_val')
            M = witness.get('M')
            N = witness.get('N', sp.zeros(A.shape[0]) if hasattr(A, 'shape') else None)
        else:
            if len(witness) == 4:
                A, lambda_val, M, N = witness
            elif len(witness) == 3:
                A, lambda_val, M = witness
                N = sp.zeros(A.shape[0]) if hasattr(A, 'shape') else None
            else:
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: A is an n × n matrix over ℝ
    try:
        h1 = isinstance(A, sp.MatrixBase) and A.is_square
        if h1:
            for val in A:
                if not sp.sympify(val).is_real:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: λ = α + iβ is an eigenvalue of A
    try:
        h2 = False
        if h1:
            n = A.shape[0]
            # Exact check
            if sp.simplify((A - lambda_val * sp.eye(n)).det()) == 0:
                h2 = True
            else:
                # Numeric check
                eigs = A.eigenvals()
                for e in eigs:
                    try:
                        diff = sp.N(e - lambda_val)
                        if abs(complex(diff)) < 1e-7:
                            h2 = True
                            break
                    except TypeError:
                        continue
    except Exception:
        h2 = False

    # H3: M is the symmetric part (A + A^T)/2
    try:
        h3 = False
        if h1 and isinstance(M, sp.MatrixBase) and M.shape == A.shape:
            expected_M = (A + A.T) / 2
            diff = M - expected_M
            if sp.simplify(diff).is_zero_matrix:
                h3 = True
            else:
                # Numeric check
                try:
                    if all(abs(complex(sp.N(val))) < 1e-7 for val in diff):
                        h3 = True
                except TypeError:
                    pass
    except Exception:
        h3 = False

    # neg_Q: α is bounded by the minimum and maximum eigenvalues of M, and |β| ≤ ρ(N) where ρ(N) is the spectral radius of N
    try:
        neg_q = False
        if h1 and isinstance(M, sp.MatrixBase) and isinstance(N, sp.MatrixBase):
            alpha = sp.re(lambda_val)
            beta = sp.im(lambda_val)
            
            M_eigs = M.eigenvals().keys()
            M_eigs_real = []
            for e in M_eigs:
                try:
                    M_eigs_real.append(float(sp.re(sp.N(e))))
                except TypeError:
                    pass
            
            if M_eigs_real:
                min_M_f = min(M_eigs_real)
                max_M_f = max(M_eigs_real)
                
                N_eigs = N.eigenvals().keys()
                N_eigs_abs = []
                for e in N_eigs:
                    try:
                        N_eigs_abs.append(abs(complex(sp.N(e))))
                    except TypeError:
                        pass
                rho_N_f = max(N_eigs_abs) if N_eigs_abs else 0.0
                
                try:
                    alpha_f = float(sp.N(alpha))
                    beta_f = float(sp.N(beta))
                    
                    fails_cond1 = (alpha_f < min_M_f - 1e-7) or (alpha_f > max_M_f + 1e-7)
                    fails_cond2 = abs(beta_f) > rho_N_f + 1e-7
                    
                    neg_q = fails_cond1 or fails_cond2
                except TypeError:
                    pass
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n × n matrix over ℝ",
    "H_2: λ = α + iβ is an eigenvalue of A",
    "H_3: M is the symmetric part (A + A^T)/2",
    "¬Q: α is not bounded by the eigenvalues of M, or |β| > ρ(N)"
]

N_HYP = 3
NEG_Q_INDEX = 3