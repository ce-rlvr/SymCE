import sympy
from sympy import Matrix, Symbol, rem, eye, zeros
from sympy.abc import x

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        
        A, W_info = witness
        
        # H1: A is an n x n matrix over a field F
        h1 = isinstance(A, Matrix) and A.is_square and A.shape[0] > 0
        
        if not h1:
            return [False, False, False]
            
        # H2: A|_W denotes the linear transformation induced by restricting A to W
        # We attempt to construct the matrix representing A|_W
        A_W = None
        if type(W_info) is int:
            k = W_info
            if 0 < k < A.shape[0]:
                A_W = A[:k, :k]
        elif isinstance(W_info, (list, tuple)):
            if len(W_info) > 0 and all(type(i) is int for i in W_info):
                A_W = A.extract(W_info, W_info)
            elif len(W_info) > 0 and all(isinstance(v, Matrix) for v in W_info):
                W_mat = Matrix.hstack(*W_info)
                A_W = (W_mat.T * W_mat).inv() * W_mat.T * A * W_mat
        elif isinstance(W_info, Matrix):
            W_mat = W_info
            A_W = (W_mat.T * W_mat).inv() * W_mat.T * A * W_mat
            
        if A_W is None or not A_W.is_square or A_W.shape[0] == 0:
            return [True, False, False]
            
        h2 = True
        
        # Conclusion: The characteristic polynomial of A|_W divides the characteristic polynomial of A
        # We check if it FAILS (neg_q = True)
        pA = A.charpoly(x).as_expr()
        pAW = A_W.charpoly(x).as_expr()
        
        remainder = rem(pA, pAW, x)
        neg_q = bool(sympy.simplify(remainder) != 0)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "H_2: A|_W denotes the linear transformation induced by restricting A to W",
    "¬Q: The characteristic polynomial of A|_W does not divide the characteristic polynomial of A"
]

N_HYP = 2
NEG_Q_INDEX = 2