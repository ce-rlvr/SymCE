import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            B = Matrix(witness['B'])
            C = Matrix(witness['C'])
            P = Matrix(witness['P'])
        else:
            B = Matrix(witness[0])
            C = Matrix(witness[1])
            P = Matrix(witness[2])
            
        # H1: V is a finite-dimensional vector space over a field F
        # We verify this by checking that B, C, and P are square matrices of the same dimension.
        h1 = bool(B.is_square and C.is_square and P.is_square and B.shape == C.shape == P.shape)
        
        if not h1:
            return [False, False, False, False]
            
        # H2: B and C are ordered bases for V
        # They must be invertible matrices.
        h2 = bool(B.det() != 0 and C.det() != 0)
        
        # H3: B^* and C^* are the respective dual bases for V^*
        # For the conclusion to be evaluated, P must be invertible.
        h3 = bool(P.det() != 0)
        
        if not (h2 and h3):
            return [h1, h2, h3, False]
            
        # The transition matrix from B to C is C^{-1} * B.
        # The transition matrix from B^* to C^* is ((C^{-1} * B)^{-1})^T = (B^{-1} * C)^T.
        actual_transition = (B.inv() * C).T
        
        # The claimed transition matrix in the false conjecture is (P^{-1})^T.
        claimed_transition = (P.inv()).T
        
        # The conclusion fails if the actual transition matrix does not equal the claimed one.
        neg_q = bool(actual_transition != claimed_transition)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B and C are ordered bases for V",
    "H_3: B^* and C^* are the respective dual bases for V^*",
    "¬Q: The transition matrix from B^* to C^* is not (P^{-1})^T"
]

N_HYP = 3
NEG_Q_INDEX = 3