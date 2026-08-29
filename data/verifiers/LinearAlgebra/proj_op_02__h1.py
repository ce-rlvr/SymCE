import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        P, x = witness
    except Exception:
        return [False, False, False]
        
    # Attempt to normalize x to a column Matrix if it was provided as a list/tuple
    try:
        if isinstance(x, (list, tuple)):
            x = Matrix(x)
            if x.shape[0] == 1:
                x = x.T
    except Exception:
        pass

    # H_1: P is a projection operator on V
    # Note: For the conjecture to be false, the dropped hypothesis must have been the one 
    # enforcing idempotence (P^2 = P). Thus, we interpret the remaining hypothesis as P 
    # being a valid linear operator (square matrix) on V.
    try:
        h1 = isinstance(P, Matrix) and P.is_square
    except Exception:
        h1 = False
        
    # H_2: x is a vector in V
    try:
        h2 = isinstance(x, Matrix) and x.shape[0] == P.shape[0] and x.shape[1] == 1
    except Exception:
        h2 = False
        
    # ¬Q: x is in the range of P if and only if Px = x (must fail at the witness)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # x is in the range of P iff the rank of P equals the rank of the augmented matrix [P | x]
            P_rank = P.rank()
            Px_rank = P.row_join(x).rank()
            x_in_range = (P_rank == Px_rank)
            
            # Check if Px = x
            diff = P * x - x
            Px_eq_x = diff.is_zero_matrix
            if Px_eq_x is None:
                Px_eq_x = all(diff[i, j] == 0 for i in range(diff.rows) for j in range(diff.cols))
                
            # The conclusion is an iff statement. We negate it by checking if the two sides differ.
            neg_q = bool(x_in_range != Px_eq_x)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is a projection operator on V",
    "H_2: x is a vector in V",
    "¬Q: x is in the range of P if and only if Px = x is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2