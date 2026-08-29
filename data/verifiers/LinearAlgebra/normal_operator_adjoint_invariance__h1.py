import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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
    "H_1: T is a normal linear operator",
    "H_2: W is a T-invariant subspace",
    "¬Q: W is not invariant under the adjoint operator T^*"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_invariant(T, W):
    """
    Checks if the subspace spanned by the columns of W is invariant under T.
    """
    if hasattr(W, 'is_invariant'):
        return W.is_invariant(T)
    
    TW = T * W
    # Create an augmented matrix [W | T*W]
    aug = W.row_join(TW)
    # Find the pivot columns
    rref_matrix, pivots = aug.rref()
    
    # If all pivot columns are within the original W, then the column space 
    # of T*W is contained in the column space of W.
    return all(p < W.cols for p in pivots)

def conditions(witness):
    T_star = None
    
    # Extract T, W, and optionally T_star or the inner product matrix M
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            W = witness.get('W')
            if 'T_star' in witness:
                T_star = witness['T_star']
            elif 'M' in witness:
                M = witness['M']
                T_star = M.inv() * T.H * M
        elif isinstance(witness, tuple):
            T = witness[0]
            W = witness[1]
            if len(witness) >= 3:
                T_star = witness[2]
        else:
            T = witness.T
            W = witness.W
    except Exception:
        return [False, False, False]

    # Determine the adjoint operator T^* if not explicitly provided
    if T_star is None:
        try:
            if hasattr(T, 'adjoint'):
                T_star = T.adjoint()
            else:
                T_star = T.H
        except Exception:
            try:
                # Fallback for fields where .H might not be supported (e.g., some finite fields)
                T_star = T.T
            except Exception:
                pass

    # H_1: T is a normal linear operator (T * T^* = T^* * T)
    try:
        if hasattr(T, 'is_normal'):
            h1_ok = bool(T.is_normal(T_star))
        else:
            h1_ok = bool(T * T_star == T_star * T)
    except Exception:
        h1_ok = False

    # H_2: W is a T-invariant subspace
    try:
        h2_ok = bool(is_invariant(T, W))
    except Exception:
        h2_ok = False

    # ¬Q: W is NOT invariant under the adjoint operator T^*
    try:
        neg_q_ok = not bool(is_invariant(T_star, W))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]