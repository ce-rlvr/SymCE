import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            U = witness.get('U')
        elif isinstance(witness, (tuple, list)) and len(witness) >= 2:
            A = witness[0]
            U = witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(A, sympy.MatrixBase) and isinstance(U, sympy.MatrixBase)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            r = A.rank()
            if U.rows != A.rows or U.cols < r:
                neg_q = True
            else:
                U_r = U[:, :r]
                diff = U_r.H * U_r - sympy.eye(r)
                diff.simplify()
                
                if diff.is_zero_matrix:
                    ortho = True
                else:
                    ortho = True
                    for i in range(diff.rows):
                        for j in range(diff.cols):
                            if sympy.simplify(diff[i, j]) != 0:
                                ortho = False
                                break
                        if not ortho:
                            break
                            
                if not ortho:
                    neg_q = True
                else:
                    A_U = A.row_join(U_r)
                    if A_U.rank() == r:
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over C and U is a matrix",
    "¬Q: The first r columns of U DO NOT form an orthonormal basis for the range of A"
]

N_HYP = 1
NEG_Q_INDEX = 1