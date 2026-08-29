import sympy
from sympy import Matrix, symbols, eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Non-commutative symbols for constructing matrices over skew fields / non-commutative rings
nc_x, nc_y, nc_z = symbols('nc_x nc_y nc_z', commutative=False)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a matrix T (or a tuple (T, T_star)) representing a linear map 
    between finite-dimensional vector spaces.
    """
    try:
        # Unpack witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                T, T_star = witness
            elif len(witness) == 4:
                _, _, T, T_star = witness
            else:
                T = witness[0]
                T_star = witness[1]
        else:
            T = witness
            if hasattr(T, 'transpose'):
                T_star = T.transpose()
            elif hasattr(T, 'T'):
                T_star = T.T
            else:
                T_star = None
    except Exception:
        return [False, False, False]

    # H_1: V and W are finite-dimensional vector spaces
    # We verify this by checking if T and T_star are matrices (which map between F^n and F^m)
    try:
        h1 = hasattr(T, 'shape') and hasattr(T_star, 'shape') and len(T.shape) == 2 and len(T_star.shape) == 2
    except Exception:
        h1 = False

    # H_2: T^* is the dual map of T
    # In matrix representation, the dual map corresponds to the transpose
    try:
        if hasattr(T, 'transpose'):
            expected_T_star = T.transpose()
        elif hasattr(T, 'T'):
            expected_T_star = T.T
        else:
            expected_T_star = None
            
        if expected_T_star is not None:
            h2 = bool(T_star == expected_T_star)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The rank of T^* is not equal to the rank of T
    try:
        if hasattr(T, 'rank'):
            rank_T = T.rank()
        else:
            rank_T = sympy.Matrix(T).rank()
            
        if hasattr(T_star, 'rank'):
            rank_T_star = T_star.rank()
        else:
            rank_T_star = sympy.Matrix(T_star).rank()
            
        neg_q = bool(rank_T != rank_T_star)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are finite-dimensional vector spaces",
    "H_2: T^* is the dual map of T",
    "¬Q: The rank of T^* is not equal to the rank of T"
]

N_HYP = 2
NEG_Q_INDEX = 2