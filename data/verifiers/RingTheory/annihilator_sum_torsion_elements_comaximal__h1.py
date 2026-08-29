import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def get_basis(matrices):
    if not matrices:
        return []
    flattened = [m.vec() for m in matrices]
    M = sp.Matrix.hstack(*flattened)
    _, pivots = M.rref()
    return [matrices[i] for i in pivots]

def get_rank(matrices):
    if not matrices:
        return 0
    flattened = [m.vec() for m in matrices]
    M = sp.Matrix.hstack(*flattened)
    return M.rank()

def in_span(matrices, target):
    if not matrices:
        return target.is_zero_matrix
    flattened = [m.vec() for m in matrices]
    M = sp.Matrix.hstack(*flattened)
    M_aug = sp.Matrix.hstack(M, target.vec())
    return M.rank() == M_aug.rank()

def get_annihilator(R_basis, v):
    if not R_basis:
        return []
    cols = [(R * v).vec() for R in R_basis]
    M = sp.Matrix.hstack(*cols)
    null_vecs = M.nullspace()
    ann_basis = []
    for vec in null_vecs:
        A = sp.zeros(R_basis[0].shape[0], R_basis[0].shape[1])
        for i, c in enumerate(vec):
            A += c * R_basis[i]
        ann_basis.append(A)
    return ann_basis

def conditions(witness):
    try:
        R_basis, x, y = witness
    except Exception:
        return [False, False, False]
    
    # H1: M is an R-module, x, y in M
    try:
        if not isinstance(R_basis, list) or not R_basis:
            h1 = False
        else:
            n = R_basis[0].shape[0]
            h1 = True
            for m in R_basis:
                if not isinstance(m, sp.Matrix) or m.shape != (n, n):
                    h1 = False
            if not isinstance(x, sp.Matrix) or not isinstance(y, sp.Matrix):
                h1 = False
            elif x.shape[0] != n or y.shape[0] != n or x.shape != y.shape:
                h1 = False
            
            if h1:
                basis = get_basis(R_basis)
                I = sp.eye(n)
                if not in_span(basis, I):
                    h1 = False
                if h1:
                    for A in basis:
                        for B in basis:
                            if not in_span(basis, A * B):
                                h1 = False
                                break
                        if not h1:
                            break
    except Exception:
        h1 = False

    # H2: Ann_R(x) and Ann_R(y) are comaximal in R
    try:
        if h1:
            basis = get_basis(R_basis)
            ann_x = get_annihilator(basis, x)
            ann_y = get_annihilator(basis, y)
            rank_R = len(basis)
            rank_sum = get_rank(ann_x + ann_y)
            h2 = (rank_sum == rank_R)
        else:
            h2 = False
    except Exception:
        h2 = False

    # Neg Q: Ann_R(x+y) != Ann_R(x) \cap Ann_R(y)
    try:
        if h1:
            basis = get_basis(R_basis)
            ann_x = get_annihilator(basis, x)
            ann_y = get_annihilator(basis, y)
            ann_x_plus_y = get_annihilator(basis, x + y)
            
            dim_x = len(ann_x)
            dim_y = len(ann_y)
            dim_sum = get_rank(ann_x + ann_y)
            dim_cap = dim_x + dim_y - dim_sum
            
            dim_x_plus_y = len(ann_x_plus_y)
            
            neg_q = (dim_x_plus_y != dim_cap)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is an R-module and x, y are elements of M",
    "H_2: The annihilator ideals Ann_R(x) and Ann_R(y) are comaximal in R",
    "¬Q: The annihilator of the sum Ann_R(x+y) is not equal to the intersection Ann_R(x) \\cap Ann_R(y)"
]

N_HYP = 2
NEG_Q_INDEX = 2