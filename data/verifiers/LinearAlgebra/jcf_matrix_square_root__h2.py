import sympy
from sympy import Matrix, MatrixBase, simplify, eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_val(val):
    try:
        if val == 0:
            return True
        if hasattr(val, 'is_zero') and val.is_zero is True:
            return True
        return simplify(val) == 0
    except Exception:
        return False

def has_square_root(A):
    """
    A square matrix A over C has a square root if and only if the sizes of its 
    Jordan blocks corresponding to the eigenvalue 0 can be partitioned into pairs 
    of the form {k, k} or {k+1, k}.
    """
    P, J = A.jordan_form()
    n = J.shape[0]
    blocks = []
    i = 0
    
    # Extract the sizes of Jordan blocks for eigenvalue 0
    while i < n:
        if is_zero_val(J[i, i]):
            size = 1
            while i + size < n and is_zero_val(J[i + size, i + size]) and J[i + size - 1, i + size] == 1:
                size += 1
            blocks.append(size)
            i += size
        else:
            i += 1
            
    if not blocks:
        return True
        
    # Count frequencies of each block size
    counts = {}
    for b in blocks:
        counts[b] = counts.get(b, 0) + 1
        
    max_b = max(blocks)
    
    # Greedily pair the largest available block sizes
    for m in range(max_b, 1, -1):
        c = counts.get(m, 0)
        if c >= 2:
            pairs = c // 2
            counts[m] -= 2 * pairs
        if counts.get(m, 0) == 1:
            if counts.get(m - 1, 0) >= 1:
                counts[m] -= 1
                counts[m - 1] -= 1
            else:
                return False
                
    return True

def conditions(witness):
    try:
        if not isinstance(witness, MatrixBase):
            A = Matrix(witness)
        else:
            A = witness
    except Exception:
        A = witness

    # H_1: A is an n x n matrix over C
    try:
        h1 = isinstance(A, MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # neg_Q: A does NOT have a square root
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not has_square_root(A)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix over C",
    "¬Q: A does not have a square root"
]

N_HYP = 1
NEG_Q_INDEX = 1