import sympy
from sympy.matrices import MatrixBase, zeros, eye

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, c = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(A, MatrixBase) and A.is_square
    except Exception:
        h1 = False
        
    try:
        if h1 and not isinstance(c, (MatrixBase, list, tuple)):
            n = A.shape[0]
            h2 = True
            for i in range(n):
                row_sum = sum([A[i, j] for j in range(n)])
                if sympy.simplify(row_sum - c) != 0:
                    h2 = False
                    break
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        if h1:
            dummy_x = sympy.Dummy('x')
            p = A.charpoly(dummy_x)
            val = p.eval(c)
            neg_q = bool(sympy.simplify(val) != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: The sum of the entries in each row of A is exactly c",
    "¬Q: p(c) != 0, where p is the characteristic polynomial of A"
]

N_HYP = 2
NEG_Q_INDEX = 2