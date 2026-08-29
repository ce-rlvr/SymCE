import sympy as sp
from sympy import Matrix, eye, zeros

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys:
      'V': Matrix whose columns span the vector space V (or int n for F^n)
      'W': Matrix whose columns span the vector space W (or int m for F^m)
      'S': Matrix whose columns are the vectors in the set S
      'f': Matrix whose columns are the target vectors f(v_i), or a callable f(v)
    """
    def parse_matrix(X):
        if isinstance(X, int):
            return eye(X)
        if isinstance(X, list) and len(X) > 0 and isinstance(X[0], Matrix):
            return Matrix.hstack(*X)
        return Matrix(X)

    try:
        V = parse_matrix(witness['V'])
        W = parse_matrix(witness['W'])
        S = parse_matrix(witness['S'])
        
        if callable(witness.get('f')):
            if S.cols > 0:
                f_cols = [parse_matrix(witness['f'](S[:, i])) for i in range(S.cols)]
                f = Matrix.hstack(*f_cols)
            else:
                f = zeros(W.rows, 0)
        else:
            f = parse_matrix(witness['f'])
            
        if S.cols != f.cols:
            return [False, False, False]
            
        if V.rows != S.rows or W.rows != f.rows:
            return [False, False, False]
            
        # H_1: V and W are vector spaces over F, and S is a subset of V.
        # S is a subset of V iff the column space of S is contained in the column space of V.
        V_S = V.row_join(S)
        h1 = bool(V.rank() == V_S.rank())
        
        # H_2: S is a linearly independent subset of V.
        # S is linearly independent iff its columns are linearly independent.
        h2 = bool(S.rank() == S.cols)
        
        # ¬Q: There does NOT exist a linear transformation T: V -> W such that T(v_i) = f(v_i).
        # Since S is linearly independent, such a T exists if and only if all f(v_i) are in W.
        # Therefore, T does NOT exist iff f is not entirely contained in W.
        W_f = W.row_join(f)
        neg_q = bool(W.rank() < W_f.rank())
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over F, and S is a subset of V",
    "H_2: S is a linearly independent subset of V",
    "¬Q: There does not exist a linear transformation T: V -> W such that T(v_i) = f(v_i)"
]

N_HYP = 2
NEG_Q_INDEX = 2