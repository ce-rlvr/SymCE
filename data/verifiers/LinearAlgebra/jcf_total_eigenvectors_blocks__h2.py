import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h1 = False

    try:
        eigenvects = witness.eigenvects()
        num_eigenvects = sum(len(vects) for evalue, mult, vects in eigenvects)
        
        P, J = witness.jordan_form()
        n = J.rows
        if n == 0:
            num_blocks = 0
        else:
            num_blocks = n - sum(1 for i in range(n - 1) if J[i, i+1] == 1)
            
        neg_q = bool(num_eigenvects != num_blocks)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over C",
    "¬Q: The total number of linearly independent eigenvectors of A is not exactly equal to the total number of Jordan blocks in J"
]

N_HYP = 1
NEG_Q_INDEX = 1