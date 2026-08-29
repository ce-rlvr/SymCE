import sympy
from sympy.matrices import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: V is a finite-dimensional vector space
    try:
        h1 = bool(hasattr(witness, 'is_square') and witness.is_square and hasattr(witness, 'columnspace'))
    except Exception:
        h1 = False

    # H_2: ker(T) = ker(T^2)
    try:
        if h1:
            T2 = witness * witness
            # In finite dimensions, ker(T) = ker(T^2) is equivalent to rank(T) = rank(T^2)
            h2 = bool(witness.rank() == T2.rank())
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: ker(T) ∩ im(T) ≠ {0}
    try:
        if h1:
            col_space = witness.columnspace()
            null_space = witness.nullspace()
            if not col_space or not null_space:
                neg_q = False
            else:
                # The dimension of the intersection of two subspaces A and B is given by
                # dim(A) + dim(B) - dim(A + B).
                M = Matrix.hstack(*(col_space + null_space))
                inter_dim = len(col_space) + len(null_space) - M.rank()
                neg_q = bool(inter_dim > 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: ker(T) = ker(T^2)",
    "¬Q: ker(T) ∩ im(T) ≠ {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2