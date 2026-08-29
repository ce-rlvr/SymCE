import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, list):
            witness = Matrix(witness)
        neg_q = not witness.is_square
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A cannot be written as a linear combination of n x n unitary matrices (e.g., A is not square)"
]

N_HYP = 0
NEG_Q_INDEX = 0