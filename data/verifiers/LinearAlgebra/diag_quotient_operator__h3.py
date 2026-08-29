import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            W = witness.get('W')
        else:
            T, W = witness
            
        if not isinstance(T, Matrix):
            T = Matrix(T)
            
        if isinstance(W, list):
            if len(W) == 0:
                W = zeros(T.rows, 1)
            elif isinstance(W[0], Matrix):
                W = Matrix.hstack(*W)
            else:
                W = Matrix(W)
        elif not isinstance(W, Matrix):
            W = Matrix(W)
    except Exception:
        return [False, False, False]

    # H_1: V is a finite-dimensional vector space
    try:
        h1 = T.is_square and T.rows == W.rows
    except Exception:
        h1 = False

    # H_2: T is a diagonalizable linear operator on V
    try:
        h2 = bool(T.is_diagonalizable())
    except Exception:
        h2 = False

    # ¬Q: The induced quotient operator of T on V/W is not diagonalizable (or not well-defined)
    try:
        if not h1:
            neg_q = False
        else:
            W_cols = W.columnspace()
            if not W_cols:
                is_invariant = True
            else:
                W_basis = Matrix.hstack(*W_cols)
                augmented = Matrix.hstack(W_basis, T * W_basis)
                is_invariant = (augmented.rank() == W_basis.rank())
            
            if not is_invariant:
                # If W is not T-invariant, the quotient operator is not well-defined,
                # hence it is not a diagonalizable operator.
                q_holds = False
            else:
                n = T.rows
                r = len(W_cols)
                if r == n or r == 0:
                    q_holds = True
                else:
                    basis_V = list(W_cols)
                    basis_extend = []
                    I = eye(n)
                    current_rank = r
                    for i in range(n):
                        v = I[:, i]
                        test_matrix = Matrix.hstack(*(basis_V + [v]))
                        if test_matrix.rank() > current_rank:
                            basis_V.append(v)
                            basis_extend.append(v)
                            current_rank += 1
                            if current_rank == n:
                                break
                    
                    B = Matrix.hstack(*basis_V)
                    T_quot_cols = []
                    for v in basis_extend:
                        X = B.LUsolve(T * v)
                        # The coordinates corresponding to the extended basis vectors
                        # represent the action of T on the quotient space V/W
                        T_quot_cols.append(X[r:, 0])
                    
                    T_quot = Matrix.hstack(*T_quot_cols)
                    q_holds = bool(T_quot.is_diagonalizable())
            neg_q = not q_holds
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: T is a diagonalizable linear operator on V",
    "¬Q: The induced quotient operator of T on V/W is not diagonalizable (or not well-defined)"
]

N_HYP = 2
NEG_Q_INDEX = 2