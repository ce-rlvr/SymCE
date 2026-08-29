import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is non-degenerate",
    "H_3: W is a subspace of V",
    "H_4: W is a totally isotropic subspace with respect to B",
    "¬Q: The dimension of W is strictly greater than half the dimension of V"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, dict):
            B = witness.get('B')
            W = witness.get('W')
        else:
            B, W = witness
            
        if not isinstance(B, Matrix):
            B = Matrix(B)
            
        # H_1: V is a finite-dimensional vector space over a field F
        h1 = B.is_square
        n = B.shape[0]
        
        # H_2: B is non-degenerate
        h2 = B.det() != 0
        
        # H_3: W is a subspace of V
        if isinstance(W, (list, tuple)):
            if len(W) == 0:
                M_W = zeros(n, 0)
            else:
                W_mats = [Matrix(w) for w in W]
                M_W = Matrix.hstack(*W_mats)
        else:
            M_W = Matrix(W)
            
        h3 = M_W.shape[0] == n
        
        # H_4: W is a totally isotropic subspace with respect to B
        # This means B(x, x) = 0 for all x in W.
        # Equivalently, the restriction of B to W is a skew-symmetric matrix with zero diagonal.
        if not h3:
            h4 = False
        else:
            A = M_W.T * B * M_W
            is_skew = True
            for i in range(A.shape[0]):
                if not (A[i, i] == 0 or sympy.simplify(A[i, i]) == 0):
                    is_skew = False
                    break
                for j in range(i + 1, A.shape[1]):
                    val = A[i, j] + A[j, i]
                    if not (val == 0 or sympy.simplify(val) == 0):
                        is_skew = False
                        break
            h4 = is_skew
            
        # ¬Q: The dimension of W is strictly greater than half the dimension of V
        if not h3:
            neg_q = False
        else:
            dim_W = M_W.rank()
            neg_q = dim_W > n / 2
            
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]