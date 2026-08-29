import sympy
from sympy import Matrix
import itertools
import math

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        # Witness can be (Q, W, p) or (Q, W)
        # Q: matrix of the quadratic form
        # W: matrix whose columns span the subspace, or list of basis vectors
        # p: characteristic of the field (default 0 for Q/R)
        if isinstance(witness, tuple):
            if len(witness) == 3:
                Q, W, p = witness
                p = int(p)
            elif len(witness) == 2:
                Q, W = witness
                p = 0
            else:
                return [False, False, False]
        else:
            return [False, False, False]
        
        Q = Matrix(Q)
        
        if isinstance(W, list):
            if len(W) == 0:
                W = sympy.zeros(Q.shape[0], 0)
            else:
                cols = []
                for v in W:
                    col = Matrix(v)
                    if col.shape[1] != 1:
                        col = col.reshape(col.shape[0]*col.shape[1], 1)
                    cols.append(col)
                W = Matrix.hstack(*cols)
        else:
            W = Matrix(W)
            
        n = Q.shape[0]
        k = W.shape[1]
        
        if Q.shape != (n, n) or W.shape[0] != n:
            return [False, False, False]
            
        # Polar bilinear form matrix B
        B = Q + Q.T
        if p > 0:
            B = B.applyfunc(lambda x: x % p)
            
        # H_1: q is a non-degenerate quadratic form on V
        # A quadratic form is non-degenerate if its radical is trivial.
        # rad(q) = {x in rad(B) | q(x) = 0}
        is_non_degenerate = True
        if p > 0:
            if p**n > 100000:
                return [False, False, False]
            for tup in itertools.product(range(p), repeat=n):
                v = Matrix(n, 1, tup)
                Bv = B * v
                if all(x % p == 0 for x in Bv):
                    # v is in rad(B)
                    if not all(x == 0 for x in v):
                        qv = (v.T * Q * v)[0] % p
                        if qv == 0:
                            is_non_degenerate = False
                            break
        else:
            if len(B.nullspace()) > 0:
                is_non_degenerate = False
                
        # H_2: W is a totally isotropic subspace of V
        # A subspace is totally isotropic if the polar form B vanishes on it: B(W, W) = 0
        W_B_W = W.T * B * W
        if p > 0:
            is_totally_isotropic = all(x % p == 0 for x in W_B_W)
        else:
            is_totally_isotropic = W_B_W.is_zero_matrix
            
        # Compute the dimension of W
        if p > 0:
            if p**k > 100000:
                return [False, False, False]
            span_W = set()
            for tup in itertools.product(range(p), repeat=k):
                c = Matrix(k, 1, tup)
                Wc = W * c
                Wc_mod = tuple(x % p for x in Wc)
                span_W.add(Wc_mod)
            dim_W = round(math.log(len(span_W), p))
        else:
            dim_W = W.rank()
            
        # ¬Q: The dimension of W is strictly greater than n/2
        neg_Q = dim_W > n / 2.0
        
        return [bool(is_non_degenerate), bool(is_totally_isotropic), bool(neg_Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: q is a non-degenerate quadratic form on V",
    "H_2: W is a totally isotropic subspace of V",
    "¬Q: The dimension of W is strictly greater than n/2"
]

N_HYP = 2
NEG_Q_INDEX = 2