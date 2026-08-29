import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: J is a k x k Jordan block with eigenvalue λ acting on a vector space V",
    "H_2: W is a non-zero J-invariant subspace of V",
    "¬Q: W is NOT spanned by {e_1, e_2, ..., e_m} for any integer m with 1 <= m <= k"
]

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        J_in, W_in = witness
    except Exception:
        return [False, False, False]
        
    try:
        if not isinstance(J_in, Matrix):
            J = Matrix(J_in)
        else:
            J = J_in
            
        if isinstance(W_in, list):
            if all(isinstance(v, Matrix) for v in W_in):
                W_mat = Matrix.hstack(*W_in)
            else:
                W_mat = Matrix(W_in)
        else:
            if not isinstance(W_in, Matrix):
                W_mat = Matrix(W_in)
            else:
                W_mat = W_in
    except Exception:
        return [False, False, False]

    # H_1: J is a k x k Jordan block with eigenvalue λ
    # We accept both upper and lower triangular Jordan blocks, as the dropped hypothesis
    # in the false conjecture is that the Jordan block must be upper triangular.
    h1 = False
    try:
        if J.is_square and J.shape[0] > 0:
            k = J.shape[0]
            lmbda = J[0, 0]
            upper = True
            lower = True
            for i in range(k):
                for j in range(k):
                    val = J[i, j]
                    if i == j:
                        if val != lmbda:
                            upper = False
                            lower = False
                    elif j == i + 1:
                        if val != 1: upper = False
                        if val != 0: lower = False
                    elif i == j + 1:
                        if val != 1: lower = False
                        if val != 0: upper = False
                    else:
                        if val != 0:
                            upper = False
                            lower = False
            h1 = upper or lower
    except Exception:
        h1 = False

    # H_2: W is a non-zero J-invariant subspace of V
    h2 = False
    try:
        if h1 and W_mat.shape[0] == J.shape[0]:
            rank_W = W_mat.rank()
            if rank_W > 0:
                # Check if J * W is contained in the span of W
                M2 = W_mat.row_join(J * W_mat)
                if M2.rank() == rank_W:
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: W is NOT spanned by {e_1, e_2, ..., e_m} for any integer m with 1 <= m <= k
    neg_q = False
    try:
        if h1 and h2:
            k = J.shape[0]
            rank_W = W_mat.rank()
            m = rank_W
            
            # If W is spanned by the first m standard basis vectors, its rank must be m,
            # and the matrix [W, E_m] must also have rank m.
            I = eye(k)
            E_m = I[:, :m]
            M = W_mat.row_join(E_m)
            is_spanned = (M.rank() == m)
            neg_q = not is_spanned
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]