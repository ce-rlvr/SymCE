import sympy
from sympy import eye, zeros, Matrix, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sympy.MatrixBase):
            witness = sympy.Matrix(witness)
            
        if witness.rows != witness.cols:
            return [False]
            
        n = witness.rows
        if n == 0:
            return [False]
            
        prod = witness * witness.H
        identity = eye(n)
        
        is_unitary = True
        for i in range(n):
            for j in range(n):
                if sympy.simplify(prod[i, j] - identity[i, j]) != 0:
                    is_unitary = False
                    break
            if not is_unitary:
                break
                
        neg_q = not is_unitary
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: U is not unitary (hence cannot be written as e^{iH} for any Hermitian H)"
]

N_HYP = 0
NEG_Q_INDEX = 0