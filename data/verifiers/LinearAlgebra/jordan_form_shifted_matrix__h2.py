import sympy
from sympy import MatrixBase, eye, simplify, Expr, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_equal(a, b):
    try:
        diff = simplify(a - b)
        if diff == 0:
            return True
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
        if abs(complex(diff)) < 1e-9:
            return True
    except Exception:
        pass
    return False

def get_blocks(J):
    blocks = []
    n = J.shape[0]
    i = 0
    while i < n:
        val = J[i, i]
        size = 1
        while i + size < n and is_equal(J[i + size - 1, i + size], 1) and is_equal(J[i + size, i + size], val):
            size += 1
        blocks.append((val, size))
        i += size
    return blocks

def multisets_match(blocks1, blocks2):
    if len(blocks1) != len(blocks2):
        return False
    used = [False] * len(blocks2)
    for v1, s1 in blocks1:
        found = False
        for i, (v2, s2) in enumerate(blocks2):
            if not used[i] and s1 == s2 and is_equal(v1, v2):
                used[i] = True
                found = True
                break
        if not found:
            return False
    return True

def conditions(witness):
    try:
        A, c = witness
    except Exception:
        return [False, False, False]
        
    # H_1: A is an n x n matrix over an algebraically closed field F
    try:
        if isinstance(A, (list, tuple)):
            A_mat = sympy.Matrix(A)
        else:
            A_mat = A
        h1 = isinstance(A_mat, MatrixBase) and A_mat.is_square
    except Exception:
        h1 = False
        
    # H_2: c is a scalar in F
    try:
        h2 = isinstance(c, (int, float, complex, Expr)) and not isinstance(c, (MatrixBase, list, tuple))
    except Exception:
        h2 = False
        
    # neg_Q: The Jordan canonical form of A + cI is NOT J + cI possessing the exact same block structure
    try:
        if not h1:
            neg_q = False
        else:
            n = A_mat.shape[0]
            I = eye(n)
            
            _, J_A = A_mat.jordan_form()
            blocks_A = get_blocks(J_A)
            
            _, J_AcI = (A_mat + c*I).jordan_form()
            blocks_AcI = get_blocks(J_AcI)
            
            expected_blocks = [(val + c, size) for val, size in blocks_A]
            
            match = multisets_match(expected_blocks, blocks_AcI)
            neg_q = not match
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over an algebraically closed field F",
    "H_2: c is a scalar in F",
    "¬Q: The Jordan canonical form of A + cI is not J + cI with shifted eigenvalues"
]

N_HYP = 2
NEG_Q_INDEX = 2