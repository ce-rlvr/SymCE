import sympy
from sympy import I, pi, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: U is a unitary matrix
    h1_ok = False
    try:
        if isinstance(witness, sympy.MatrixBase) and witness.shape[0] == witness.shape[1]:
            n = witness.shape[0]
            diff = sympy.simplify(witness.H * witness - eye(n))
            if diff == zeros(n, n):
                h1_ok = True
            else:
                try:
                    diff_n = diff.evalf()
                    is_zero = True
                    for i in range(n):
                        for j in range(n):
                            if abs(complex(diff_n[i, j])) > 1e-9:
                                is_zero = False
                                break
                    if is_zero:
                        h1_ok = True
                except Exception:
                    pass
    except Exception:
        pass

    # neg_Q: The principal matrix logarithm of U is not a skew-Hermitian matrix
    neg_q_ok = False
    try:
        if isinstance(witness, sympy.MatrixBase) and witness.shape[0] == witness.shape[1]:
            eigenvals = witness.eigenvals()
            has_neg_real = False
            for val in eigenvals.keys():
                try:
                    val_simp = sympy.simplify(val)
                    if val_simp.is_real == True and bool(val_simp <= 0):
                        has_neg_real = True
                        break
                except Exception:
                    pass
                
                try:
                    im_val = sympy.simplify(sympy.im(val_simp))
                    re_val = sympy.simplify(sympy.re(val_simp))
                    if im_val == 0 and bool(re_val <= 0):
                        has_neg_real = True
                        break
                except Exception:
                    pass
                
                try:
                    val_n = complex(val.evalf())
                    if abs(val_n.imag) < 1e-9 and val_n.real <= 1e-10:
                        has_neg_real = True
                        break
                except Exception:
                    pass
            
            if has_neg_real:
                # The principal logarithm is undefined for matrices with eigenvalues on the negative real axis
                neg_q_ok = True
            else:
                try:
                    P, D = witness.diagonalize()
                    logD = sympy.diag(*[sympy.log(D[i, i]) for i in range(D.shape[0])])
                    logU = P * logD * P.inv()
                    diff = sympy.simplify(logU.H + logU)
                    if diff != zeros(*logU.shape):
                        try:
                            diff_n = diff.evalf()
                            is_zero = True
                            for i in range(diff_n.shape[0]):
                                for j in range(diff_n.shape[1]):
                                    if abs(complex(diff_n[i, j])) > 1e-9:
                                        is_zero = False
                                        break
                            if not is_zero:
                                neg_q_ok = True
                        except Exception:
                            neg_q_ok = True
                except Exception:
                    pass
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: The principal matrix logarithm of U is not a skew-Hermitian matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1