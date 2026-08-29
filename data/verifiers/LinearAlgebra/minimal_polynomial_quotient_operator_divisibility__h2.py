import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x

# Top-level setup for standard algebra objects
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is "T is a linear operator on V".
    Without it, T might not map V to V, making the quotient operator T/W undefined.
    """
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            V = witness.get('V')
            W = witness.get('W')
        else:
            T, V, W = witness
            
        T = Matrix(T)
        n = T.shape[0]
        
        def to_matrix(obj, default_rows):
            if isinstance(obj, Matrix):
                return obj
            if isinstance(obj, (list, tuple)):
                if len(obj) > 0:
                    if isinstance(obj[0], Matrix):
                        return Matrix.hstack(*obj)
                return Matrix(obj)
            return Matrix(obj)

        V_mat = to_matrix(V, n)
        W_mat = to_matrix(W, n)
    except Exception:
        return [False, False, False]
        
    # H1: V is a finite-dimensional vector space
    try:
        # V_mat represents a subspace (its column space) in F^n, which is finite-dimensional.
        h1 = hasattr(V_mat, 'shape') and len(V_mat.shape) == 2
    except Exception:
        h1 = False
        
    # H2: W is a T-invariant subspace of V
    try:
        # W is a subspace of V iff rank([V W]) == rank(V)
        is_subspace = V_mat.row_join(W_mat).rank() == V_mat.rank()
        # W is T-invariant iff rank([W T(W)]) == rank(W)
        is_invariant = W_mat.row_join(T * W_mat).rank() == W_mat.rank()
        h2 = is_subspace and is_invariant
    except Exception:
        h2 = False
        
    # ¬Q: The minimal polynomial of the quotient operator T/W does not divide the minimal polynomial of T.
    try:
        # For T/W to be a well-defined operator on V/W, V must be T-invariant.
        # If V is T-invariant, the minimal polynomial of T/W ALWAYS divides the minimal polynomial of T.
        # If V is NOT T-invariant, T/W is undefined on V/W, so the conclusion fails.
        is_V_invariant = V_mat.row_join(T * V_mat).rank() == V_mat.rank()
        neg_q = not is_V_invariant
    except Exception:
        # If T cannot even act on V_mat, T/W is undefined.
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: The minimal polynomial of the quotient operator T/W does not divide the minimal polynomial of T (or T/W is undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2