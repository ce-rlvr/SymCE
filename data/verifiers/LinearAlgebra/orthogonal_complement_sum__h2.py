import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_subset(S):
    if isinstance(S, Matrix):
        return S.tolist()
    rows = []
    for v in S:
        if isinstance(v, Matrix):
            rows.append(list(v))
        else:
            rows.append(list(v))
    return rows

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        
        U, W = witness
        
        U_rows = parse_subset(U)
        W_rows = parse_subset(W)
        
        if not U_rows or not W_rows:
            return [False, False]
            
        dim = len(U_rows[0])
        if dim == 0:
            return [False, False]
            
        for v in U_rows:
            if len(v) != dim: 
                return [False, False]
        for v in W_rows:
            if len(v) != dim: 
                return [False, False]
            
        h1 = True
        
        # Compute Minkowski sum U + W
        U_plus_W = []
        for u in U_rows:
            for w in W_rows:
                U_plus_W.append([u[i] + w[i] for i in range(dim)])
                
        # Orthogonal complement of U + W
        M_U_plus_W = Matrix(U_plus_W)
        perp_U_plus_W = M_U_plus_W.nullspace()
        
        # Intersection of U^perp and W^perp (which is (U union W)^perp)
        U_union_W = U_rows + W_rows
        M_U_union_W = Matrix(U_union_W)
        perp_U_cap_W = M_U_union_W.nullspace()
        
        # Check if the two orthogonal complements are equal
        if len(perp_U_plus_W) != len(perp_U_cap_W):
            neg_q = True
        else:
            if len(perp_U_plus_W) == 0:
                neg_q = False
            else:
                M_combined = Matrix.hstack(*(perp_U_plus_W + perp_U_cap_W))
                neg_q = M_combined.rank() > len(perp_U_plus_W)
                
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V is an inner product space and U, W are subsets",
    "¬Q: (U + W)^perp != U^perp ∩ W^perp"
]

N_HYP = 1
NEG_Q_INDEX = 1