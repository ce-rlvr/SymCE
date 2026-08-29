import sympy
from sympy import Matrix, MatrixBase, zeros, diag, simplify, eye
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_blocks(M):
    if M.rows == 0:
        return []
    _, J = M.jordan_form()
    n = J.rows
    blocks = []
    i = 0
    while i < n:
        eig = J[i, i]
        j = i + 1
        while j < n and simplify(J[j-1, j] - 1) == 0 and simplify(J[j, j] - eig) == 0:
            j += 1
        blocks.append((eig, j - i))
        i = j
    return blocks

def are_similar(X, Y):
    if X.shape != Y.shape:
        return False
    blocks_X = get_blocks(X)
    blocks_Y = get_blocks(Y)
    if len(blocks_X) != len(blocks_Y):
        return False
    used = [False] * len(blocks_Y)
    for bx in blocks_X:
        matched = False
        for k, by in enumerate(blocks_Y):
            if not used[k] and bx[1] == by[1] and simplify(bx[0] - by[0]) == 0:
                used[k] = True
                matched = True
                break
        if not matched:
            return False
    return True

def drazin_inverse(A):
    if A.rows == 0:
        return A
    P, J = A.jordan_form()
    n = J.rows
    JD = zeros(n, n)
    i = 0
    while i < n:
        eig = J[i, i]
        j = i + 1
        while j < n and simplify(J[j-1, j] - 1) == 0 and simplify(J[j, j] - eig) == 0:
            j += 1
        size = j - i
        block = J[i:j, i:j]
        if simplify(eig) == 0:
            JD[i:j, i:j] = zeros(size, size)
        else:
            JD[i:j, i:j] = block.inv()
        i = j
    return P * JD * P.inv()

def conditions(witness):
    if isinstance(witness, dict):
        A = witness.get('A')
        C = witness.get('C')
        N = witness.get('N')
    elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
        A, C, N = witness[:3]
    else:
        return [False, False]
    
    # H1: A is a square matrix over C
    try:
        h1 = isinstance(A, MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # neg_Q: The Drazin inverse of A is NOT similar to C^{-1} \oplus 0
    try:
        if not isinstance(C, MatrixBase) or not C.is_square:
            neg_q = False
        elif not isinstance(N, MatrixBase) or not N.is_square:
            neg_q = False
        elif C.det() == 0:
            # C is not invertible, so C^{-1} is undefined. The conclusion fails.
            neg_q = True
        else:
            C_inv = C.inv()
            Z = zeros(N.rows, N.cols)
            rhs = diag(C_inv, Z)
            AD = drazin_inverse(A)
            q = are_similar(AD, rhs)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix over C",
    "¬Q: The Drazin inverse of A is not similar to C^{-1} \\oplus 0"
]

N_HYP = 1
NEG_Q_INDEX = 1