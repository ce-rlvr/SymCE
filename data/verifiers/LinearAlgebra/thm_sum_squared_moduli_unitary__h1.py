import sympy
from sympy import Matrix, eye, zeros, I, Abs

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        U = Matrix(witness)
        n = U.rows
        
        total_sum = 0
        for i in range(U.rows):
            for j in range(U.cols):
                total_sum += Abs(U[i, j])**2
                
        diff = sympy.simplify(total_sum - n)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The sum of the squared absolute values of all entries of U is not exactly n"
]

N_HYP = 0
NEG_Q_INDEX = 0