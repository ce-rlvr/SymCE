import sympy
from sympy import Matrix, eye, zeros, oo
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
    "H_1: U and W are subspaces of V",
    "H_2: V is the direct sum of U and W",
    "¬Q: The dual space V^* is NOT isomorphic to the direct sum of the dual spaces U^* and W^*"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            V = witness.get('V')
            U = witness.get('U')
            W = witness.get('W')
        elif isinstance(witness, tuple) and len(witness) == 3:
            V, U, W = witness
        else:
            V = getattr(witness, 'V', None)
            U = getattr(witness, 'U', None)
            W = getattr(witness, 'W', None)
            
        if V is None or U is None or W is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def get_rank(space):
        if isinstance(space, int):
            return space
        if space == oo:
            return oo
        if isinstance(space, Matrix):
            return space.rank()
        if isinstance(space, list):
            try:
                return Matrix(space).rank()
            except Exception:
                pass
        return None

    dim_V = get_rank(V)
    dim_U = get_rank(U)
    dim_W = get_rank(W)

    if dim_V is None or dim_U is None or dim_W is None:
        return [False, False, False]

    # H_1: U and W are subspaces of V
    try:
        if dim_V == oo:
            h1 = True
        else:
            if isinstance(V, (Matrix, list)) and isinstance(U, (Matrix, list)) and isinstance(W, (Matrix, list)):
                mat_V = Matrix(V)
                mat_U = Matrix(U)
                mat_W = Matrix(W)
                rank_V = mat_V.rank()
                h1 = (mat_V.row_join(mat_U).rank() == rank_V) and \
                     (mat_V.row_join(mat_W).rank() == rank_V)
            else:
                h1 = (dim_U <= dim_V) and (dim_W <= dim_V)
    except Exception:
        h1 = False

    # H_2: V is the direct sum of U and W
    try:
        if dim_V == oo:
            h2 = (dim_U == oo or dim_W == oo)
        else:
            if isinstance(V, (Matrix, list)) and isinstance(U, (Matrix, list)) and isinstance(W, (Matrix, list)):
                mat_V = Matrix(V)
                mat_U = Matrix(U)
                mat_W = Matrix(W)
                rank_V = mat_V.rank()
                rank_U = mat_U.rank()
                rank_W = mat_W.rank()
                h2 = (mat_U.row_join(mat_W).rank() == rank_V) and \
                     (rank_U + rank_W == rank_V)
            else:
                h2 = (dim_V == dim_U + dim_W)
    except Exception:
        h2 = False

    # ¬Q: The dual space V^* is NOT isomorphic to the direct sum of the dual spaces U^* and W^*
    # Note: Mathematically, V^* is always isomorphic to U^* \oplus W^* for any direct sum V = U \oplus W.
    # The verifier correctly evaluates this mathematical truth.
    try:
        if dim_V == oo:
            neg_q = False
        else:
            if isinstance(V, (Matrix, list)) and isinstance(U, (Matrix, list)) and isinstance(W, (Matrix, list)):
                mat_V = Matrix(V)
                mat_U = Matrix(U)
                mat_W = Matrix(W)
                rank_V = mat_V.rank()
                rank_U = mat_U.rank()
                rank_W = mat_W.rank()
                neg_q = (rank_V != rank_U + rank_W)
            else:
                neg_q = (dim_V != dim_U + dim_W)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]