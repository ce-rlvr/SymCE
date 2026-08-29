import sympy
from sympy import Matrix, eye, zeros, simplify, MatrixBase
from sympy.abc import z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_jordan_form(J):
    if not J.is_square: return False
    n = J.shape[0]
    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            elif j == i + 1:
                val = J[i, j]
                if not (val == 0 or val == 1):
                    return False
                if val == 1 and J[i, i] != J[j, j]:
                    return False
            else:
                if J[i, j] != 0:
                    return False
    return True

def conditions(witness):
    if isinstance(witness, tuple):
        if len(witness) == 4:
            A, J, P, z_val = witness
        elif len(witness) == 3:
            A, J, P = witness
            try:
                evs = list(A.eigenvals().keys())
                z_val = evs[0] if evs else 0
            except Exception:
                z_val = 0
        else:
            return [False, False, False]
    else:
        return [False, False, False]
        
    # H1
    try:
        h1 = False
        if isinstance(A, MatrixBase) and isinstance(J, MatrixBase):
            if A.is_square and J.is_square and A.shape == J.shape:
                if is_jordan_form(J):
                    JA = A.jordan_form()[1]
                    JJ = J.jordan_form()[1]
                    diff_h1 = JA - JJ
                    diff_h1 = diff_h1.applyfunc(simplify)
                    n_shape = A.shape[0]
                    if all(diff_h1[i, j] == 0 for i in range(n_shape) for j in range(n_shape)):
                        h1 = True
    except Exception:
        h1 = False
        
    # H2
    try:
        h2 = False
        if isinstance(P, MatrixBase) and P.is_square and P.shape == A.shape:
            if simplify(P.det()) != 0:
                diff_h2 = A * P - P * J
                diff_h2 = diff_h2.applyfunc(simplify)
                n_shape = A.shape[0]
                if all(diff_h2[i, j] == 0 for i in range(n_shape) for j in range(n_shape)):
                    h2 = True
    except Exception:
        h2 = False
        
    # neg_Q
    try:
        neg_q = False
        n = A.shape[0]
        I = eye(n)
        
        detA = simplify((z_val * I - A).det())
        if detA == 0:
            neg_q = True
        else:
            resA = (z_val * I - A).inv()
            detJ = simplify((z_val * I - J).det())
            if detJ == 0:
                neg_q = True
            else:
                resJ = (z_val * I - J).inv()
                diff = resA - P * resJ * P.inv()
                diff = diff.applyfunc(simplify)
                if not all(diff[i, j] == 0 for i in range(n) for j in range(n)):
                    neg_q = True
                elif not resJ.is_upper:
                    neg_q = True
                else:
                    i = 0
                    while i < n:
                        block_size = 1
                        while i + block_size < n and J[i + block_size - 1, i + block_size] == 1:
                            block_size += 1
                            
                        for r in range(block_size):
                            for c in range(block_size):
                                if c >= r:
                                    if simplify(resJ[i+r, i+c] - resJ[i, i+(c-r)]) != 0:
                                        neg_q = True
                                        break
                                else:
                                    if simplify(resJ[i+r, i+c]) != 0:
                                        neg_q = True
                                        break
                            if neg_q: break
                        i += block_size
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over C with Jordan canonical form J",
    "H_2: P is an invertible matrix such that A = P J P^{-1}",
    "¬Q: The resolvent matrix (zI - A)^{-1} is not equal to P (zI - J)^{-1} P^{-1} or blocks of (zI - J)^{-1} are not upper triangular Toeplitz"
]

N_HYP = 2
NEG_Q_INDEX = 2