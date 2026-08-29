import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: W is a subspace of V",
    "¬Q: dim(W) + dim(W^\\perp) \\neq dim(V)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    results = []
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                # Interpretation: witness is (V, W, B) where B is the bilinear form matrix
                V, W, B = witness
                V_mat = Matrix(V)
                W_mat = Matrix(W)
                B_mat = Matrix(B)
                
                if V_mat.cols == W_mat.cols and V_mat.cols == B_mat.cols and B_mat.rows == B_mat.cols:
                    combined = V_mat.col_join(W_mat)
                    h1 = combined.rank() == V_mat.rank()
                    
                    if h1:
                        dim_V = V_mat.rank()
                        dim_W = W_mat.rank()
                        
                        V_basis = V_mat.rowspace()
                        if not V_basis:
                            dim_W_perp = 0
                        else:
                            V_basis_mat = V_basis[0]
                            for r in V_basis[1:]:
                                V_basis_mat = V_basis_mat.col_join(r)
                            # W^\perp in V is the set of x in V such that w^T B x = 0 for all w in W
                            M = W_mat * B_mat * V_basis_mat.T
                            dim_W_perp = M.cols - M.rank()
                            
                        neg_q = (dim_W + dim_W_perp) != dim_V
                        results.append([bool(h1), bool(neg_q)])
                        
            elif len(witness) == 2:
                # Interpretation 1: witness is (W, B) where V is implicitly R^n
                try:
                    W, B = witness
                    W_mat = Matrix(W)
                    B_mat = Matrix(B)
                    
                    if W_mat.cols == B_mat.cols and B_mat.rows == B_mat.cols:
                        h1_WB = True
                        dim_V = B_mat.cols
                        dim_W = W_mat.rank()
                        dim_W_perp = B_mat.cols - (W_mat * B_mat).rank()
                        neg_q_WB = (dim_W + dim_W_perp) != dim_V
                        results.append([True, bool(neg_q_WB)])
                except Exception:
                    pass
                
                # Interpretation 2: witness is (V, W) with standard inner product, 
                # but W^\perp is mistakenly taken as the orthogonal complement in R^n
                try:
                    V, W = witness
                    V_mat = Matrix(V)
                    W_mat = Matrix(W)
                    
                    if V_mat.cols == W_mat.cols:
                        combined = V_mat.col_join(W_mat)
                        h1_VW = combined.rank() == V_mat.rank()
                        
                        if h1_VW:
                            dim_V = V_mat.rank()
                            dim_W = W_mat.rank()
                            dim_W_perp = W_mat.cols - W_mat.rank()
                            neg_q_VW = (dim_W + dim_W_perp) != dim_V
                            results.append([True, bool(neg_q_VW)])
                except Exception:
                    pass

    except Exception:
        pass

    if [True, True] in results:
        return [True, True]
    if [True, False] in results:
        return [True, False]
    
    return [False, False]