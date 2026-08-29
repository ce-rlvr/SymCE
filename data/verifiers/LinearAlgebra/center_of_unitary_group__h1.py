import sympy
from sympy import eye, I

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (U, n), where U is the matrix and n is the dimension.
    If the witness is just U, n is inferred from U's shape.
    """
    try:
        if isinstance(witness, tuple):
            U, n = witness
        else:
            U = witness
            n = U.shape[0]
    except Exception:
        return [False, False, False]

    # H_1: U is a unitary matrix
    try:
        if not hasattr(U, 'shape') or U.shape[0] != U.shape[1]:
            h1_ok = False
        else:
            m = U.shape[0]
            if hasattr(U, 'H'):
                UH = U.H
            else:
                UH = U.conjugate().transpose()
            
            I_m = eye(m)
            # Check U * U^H == I and U^H * U == I
            h1_ok = bool(U * UH == I_m) and bool(UH * U == I_m)
    except Exception:
        h1_ok = False

    # H_2: For every n x n unitary matrix V, UV = VU
    try:
        h2_ok = True
        if U.shape[0] != n:
            h2_ok = False
        else:
            # Check commutation with a set of generators for the unitary group U(n)
            # 1. Permutation matrix (swaps first two basis vectors)
            if n >= 2:
                P = eye(n)
                P.row_swap(0, 1)
                if bool(U * P != P * U):
                    h2_ok = False
            # 2. Diagonal unitary matrices with different phases
            if n >= 1:
                D1 = eye(n)
                D1[0, 0] = -1
                if bool(U * D1 != D1 * U):
                    h2_ok = False
                
                D2 = eye(n)
                D2[0, 0] = I
                if bool(U * D2 != D2 * U):
                    h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: It is NOT the case that there exists a real number theta such that U = e^{i*theta} I_n
    try:
        if n == 0:
            # For n=0, U is the empty matrix, which trivially equals e^{i*theta} I_0 for any theta.
            # Thus, the conclusion holds, so its negation is False.
            neg_q_ok = False
        else:
            c = U[0, 0]
            is_scalar = True
            for i in range(n):
                for j in range(n):
                    if i == j:
                        if bool(U[i, j] != c):
                            is_scalar = False
                    else:
                        if bool(U[i, j] != 0):
                            is_scalar = False
            
            if not is_scalar:
                neg_q_ok = True
            else:
                # If U is a scalar matrix c * I_n, we check if c can be written as e^{i*theta} for real theta.
                # This is true if and only if c is a complex number with absolute value 1.
                try:
                    abs_c = sympy.simplify(sympy.Abs(c))
                    if abs_c == 1:
                        neg_q_ok = False
                    else:
                        neg_q_ok = True
                except Exception:
                    # If taking the absolute value fails (e.g., for matrices over finite fields or custom rings),
                    # it implies c is not a standard complex phase, so the conclusion fails.
                    neg_q_ok = True
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "H_2: For every n x n unitary matrix V, UV = VU",
    "¬Q: There does NOT exist a real number theta such that U = e^{i*theta} I_n"
]

N_HYP = 2
NEG_Q_INDEX = 2