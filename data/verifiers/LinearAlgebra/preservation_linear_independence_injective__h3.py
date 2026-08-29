import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a counterexample to the false conjecture:
    "If V and W are vector spaces, T is a linear map from V to W, and S is a 
    linearly independent subset of V, then T(S) is a linearly independent subset of W."
    
    A valid witness is a tuple (T, S) where:
      - T is a sympy Matrix representing the linear map.
      - S is a list/tuple of sympy Matrices (column vectors) representing the subset S.
    """
    try:
        T, S = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: V and W are vector spaces over a field F
    try:
        h1 = (isinstance(T, sympy.MatrixBase) and 
              isinstance(S, (list, tuple)) and 
              all(isinstance(v, sympy.MatrixBase) for v in S))
    except Exception:
        h1 = False

    # H_2: T is a linear map from V to W
    try:
        h2 = False
        if h1:
            # Check if dimensions are compatible for T to act on vectors in S
            if all(v.shape[1] == 1 for v in S) and all(T.shape[1] == v.shape[0] for v in S):
                h2 = True
    except Exception:
        h2 = False

    # H_3: S is a linearly independent subset of V
    try:
        h3 = False
        if h2:
            S_set = []
            for v in S:
                if not any(v == u for u in S_set):
                    S_set.append(v)
            if len(S_set) == 0:
                h3 = True
            else:
                M_S = sympy.Matrix.hstack(*S_set)
                h3 = M_S.rank() == len(S_set)
    except Exception:
        h3 = False

    # ¬Q: The image T(S) is NOT a linearly independent subset of W
    try:
        neg_q = False
        if h2:
            S_set = []
            for v in S:
                if not any(v == u for u in S_set):
                    S_set.append(v)
            
            TS_set = []
            for v in S_set:
                w = T * v
                if not any(w == u for u in TS_set):
                    TS_set.append(w)
            
            if len(TS_set) == 0:
                neg_q = False
            else:
                M_TS = sympy.Matrix.hstack(*TS_set)
                neg_q = M_TS.rank() < len(TS_set)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: T is a linear map from V to W",
    "H_3: S is a linearly independent subset of V",
    "¬Q: The image T(S) is not a linearly independent subset of W"
]

N_HYP = 3
NEG_Q_INDEX = 3