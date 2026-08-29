import sympy
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Verify the witness is a matrix
        if not hasattr(witness, 'is_Matrix') or not witness.is_Matrix:
            return [False]
        
        # The matrix exponential exp(X) is defined by a globally convergent power series.
        # It is an analytic function on M_n(R), and therefore it is infinitely 
        # differentiable (and thus continuously differentiable) at every real matrix X.
        # Since the conclusion is mathematically true for all X in M_n(R), 
        # its negation (that exp(X) is NOT continuously differentiable at X) is always False.
        neg_q = False
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: exp(X) is not continuously differentiable at X"
]

N_HYP = 0
NEG_Q_INDEX = 0