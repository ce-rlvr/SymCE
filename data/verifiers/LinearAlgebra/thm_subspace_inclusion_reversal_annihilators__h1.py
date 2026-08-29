import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: W_1 and W_2 are subspaces of V",
    "H_2: W_1^0 and W_2^0 are the annihilators of W_1 and W_2 respectively in the dual space V^*",
    "¬Q: W_1 \\subseteq W_2 \\iff W_2^0 \\subseteq W_1^0 is false"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # 1. Try generic object with properties
    try:
        h1 = bool(witness.W1_is_subspace and witness.W2_is_subspace)
        h2 = bool(witness.W1_0_is_annihilator and witness.W2_0_is_annihilator)
        q = bool(witness.W1_subset_W2) == bool(witness.W2_0_subset_W1_0)
        return [h1, h2, not q]
    except Exception:
        pass

    # 2. Try dictionary
    try:
        if isinstance(witness, dict):
            if 'h1' in witness or 'H1' in witness:
                h1 = bool(witness.get('h1', witness.get('H1', False)))
                h2 = bool(witness.get('h2', witness.get('H2', False)))
                neg_q = bool(witness.get('neg_q', witness.get('neg_Q', False)))
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try tuple of matrices (W1, W2) or (W1, W2, W1_0, W2_0) representing submodules over Z
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                W1 = Matrix(witness[0])
                W2 = Matrix(witness[1])
                W1_0, W2_0 = None, None
            elif len(witness) == 4:
                W1 = Matrix(witness[0])
                W2 = Matrix(witness[1])
                W1_0 = Matrix(witness[2])
                W2_0 = Matrix(witness[3])
            else:
                raise ValueError
                
            if hasattr(W1, 'rows') and hasattr(W2, 'rows'):
                h1 = (W1.rows == W2.rows)
                
                if W1_0 is not None and W2_0 is not None:
                    h2_1 = (W1_0 * W1).is_zero_matrix
                    h2_2 = (W2_0 * W2).is_zero_matrix
                    n = W1.rows
                    h2_3 = (W1_0.rank() + W1.rank() == n)
                    h2_4 = (W2_0.rank() + W2.rank() == n)
                    h2 = bool(h2_1 and h2_2 and h2_3 and h2_4)
                else:
                    h2 = True
                    ns1 = W1.T.nullspace()
                    ns2 = W2.T.nullspace()
                    W1_0 = Matrix([v.T for v in ns1]) if ns1 else Matrix(0, W1.rows, [])
                    W2_0 = Matrix([v.T for v in ns2]) if ns2 else Matrix(0, W2.rows, [])
                
                def is_subset(A, B):
                    if A.rows != B.rows: return False
                    if A.cols == 0: return True
                    if B.cols == 0: return A.is_zero_matrix
                    for j in range(A.cols):
                        try:
                            x = B.solve(A[:, j])
                            if not all(val.is_integer for val in x):
                                return False
                        except Exception:
                            return False
                    return True
                
                def is_subset_row(A, B):
                    if A.rows == 0: return True
                    if B.rows == 0: return A.is_zero_matrix
                    return is_subset(A.T, B.T)
                    
                w1_sub_w2 = is_subset(W1, W2)
                w2_0_sub_w1_0 = is_subset_row(W2_0, W1_0)
                
                q = (w1_sub_w2 == w2_0_sub_w1_0)
                return [h1, h2, not q]
    except Exception:
        pass

    return [False, False, False]