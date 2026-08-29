import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            v = witness.get('v')
            if T is None or v is None:
                return [False, False, False]
        else:
            T = witness[0]
            v = witness[1]
    except Exception:
        return [False, False, False]

    try:
        T_mat = sympy.Matrix(T)
        h1 = T_mat.is_square
    except Exception:
        h1 = False

    try:
        v_mat = sympy.Matrix(v)
        h2 = v_mat.shape == (T_mat.shape[0], 1)
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n = T_mat.shape[0]
            if n == 0:
                neg_q = False
            else:
                # The Krylov subspace for a finite dimensional space of dimension n
                # is spanned by the first n terms: v, T(v), ..., T^{n-1}(v)
                cols = [v_mat]
                curr = v_mat
                for _ in range(n - 1):
                    curr = T_mat * curr
                    cols.append(curr)
                
                K = sympy.Matrix.hstack(*cols)
                TK = T_mat * K
                K_TK = sympy.Matrix.hstack(K, TK)
                
                # The span is T-invariant if T*K is contained in the column space of K.
                # This is equivalent to rank(K) == rank([K, T*K]).
                # The conclusion fails (neg_q is True) if it is NOT T-invariant.
                neg_q = bool(K.rank() < K_TK.rank())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: v is a vector in V",
    "¬Q: The span of the sequence of vectors v, T(v), T^2(v), ... is not a T-invariant subspace of V"
]

N_HYP = 2
NEG_Q_INDEX = 2