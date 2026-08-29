import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not (isinstance(witness, MatrixBase) and witness.is_square):
            neg_q = False
        else:
            n = witness.rows
            k = witness.rank()
            _, J = witness.jordan_form()
            is_diagonal = J.is_diagonal()
            
            ones_count = 0
            zeros_count = 0
            for i in range(n):
                val = sympy.simplify(J[i, i])
                if val == 1:
                    ones_count += 1
                elif val == 0:
                    zeros_count += 1
                    
            conclusion_holds = is_diagonal and (ones_count == k) and (zeros_count == n - k)
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a square matrix",
    "¬Q: The Jordan canonical form of P is not a diagonal matrix with exactly k ones and n-k zeros"
]

N_HYP = 1
NEG_Q_INDEX = 1