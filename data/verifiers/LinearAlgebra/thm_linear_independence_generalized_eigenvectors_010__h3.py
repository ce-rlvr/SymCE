import sympy
from sympy import Matrix, eye

I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        T, vectors = witness
    except Exception:
        return [False, False, False]
        
    # H1: T is a square matrix representing a linear operator on V = F^n
    try:
        h1 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1 = False
        
    # H2: For each i, v_i is a non-zero generalized eigenvector of T corresponding to lambda_i
    try:
        if not h1 or not isinstance(vectors, (list, tuple)) or len(vectors) == 0:
            h2 = False
        else:
            n = T.shape[0]
            I = eye(n)
            h2 = True
            for item in vectors:
                if not isinstance(item, (list, tuple)) or len(item) != 2:
                    h2 = False
                    break
                v, l = item
                if not isinstance(v, Matrix) or v.shape != (n, 1) or v.expand().is_zero_matrix:
                    h2 = False
                    break
                diff = ((T - l*I)**n * v).expand()
                if not diff.is_zero_matrix:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # neg_Q: The set of vectors {v_1, ..., v_k} is linearly dependent
    try:
        if not isinstance(vectors, (list, tuple)) or len(vectors) == 0:
            neg_q = False
        else:
            vs = [item[0] for item in vectors]
            M = Matrix.hstack(*vs)
            neg_q = M.rank() < len(vs)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on a vector space V",
    "H_2: Each v_i is a non-zero generalized eigenvector of T for lambda_i",
    "¬Q: The set of vectors {v_1, ..., v_k} is linearly dependent"
]

N_HYP = 2
NEG_Q_INDEX = 2