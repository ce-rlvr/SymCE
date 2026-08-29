import sympy
from sympy import Matrix, eye

I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]

    try:
        if not (hasattr(A, 'is_Matrix') and A.is_Matrix and hasattr(B, 'is_Matrix') and B.is_Matrix):
            h1 = False
        elif A.shape[0] != A.shape[1]:
            h1 = False
        elif A.shape != B.shape:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    try:
        if h1:
            evs = A.eigenvects()
            h2 = all(len(evects) == 1 for ev, alg_mult, evects in evs)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            n = A.shape[0]
            vecs = []
            A_k = eye(n)
            for _ in range(n):
                vecs.append(list(A_k))
                A_k = A_k * A
            M = Matrix(vecs).T
            B_vec = Matrix(list(B))
            rank_M = M.rank()
            rank_aug = M.row_join(B_vec).rank()
            neg_q = (rank_M != rank_aug)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n matrices over C",
    "H_2: The Jordan canonical form of A has exactly one Jordan block for each distinct eigenvalue",
    "¬Q: B is not a polynomial in A"
]

N_HYP = 2
NEG_Q_INDEX = 2