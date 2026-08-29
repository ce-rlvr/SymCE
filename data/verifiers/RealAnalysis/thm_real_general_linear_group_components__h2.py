import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Given a witness (expected to be an integer n), evaluates the hypotheses and the negated conclusion.
    """
    n = witness
    
    # H_1: Let n >= 1 be an integer.
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 1
    except Exception:
        h1 = False
        
    # H_2: Equip GL(n, R) with the subspace topology inherited from R^{n x n}.
    # This is a definitional/contextual hypothesis that is vacuously true for the parameter n.
    try:
        h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: GL(n, R) is NOT (not connected and has exactly two connected components, 
    # corresponding to matrices with positive determinant and matrices with negative determinant).
    # Mathematically, for all integers n >= 1, GL(n, R) ALWAYS has exactly two connected components 
    # (GL+ and GL-) which correspond to positive and negative determinants.
    # Therefore, the conclusion is TRUE for all n >= 1, meaning its negation is FALSE.
    try:
        if isinstance(n, (int, sympy.Integer)) and n >= 1:
            neg_q = False
        else:
            # If n is not a valid integer >= 1, the conclusion about GL(n, R) having exactly 2 components fails
            # (e.g., for n=0, GL(0, R) has 1 component).
            neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: Equip GL(n, R) with the subspace topology inherited from R^{n x n}",
    "¬Q: GL(n, R) does not have exactly two connected components corresponding to positive and negative determinants"
]

N_HYP = 2
NEG_Q_INDEX = 2