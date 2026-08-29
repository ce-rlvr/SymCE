import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that any space V admits a unique orthogonal decomposition 
    into a hyperbolic space and an anisotropic space.
    This fails if V is degenerate (det == 0) or not a symmetric bilinear space.
    """
    try:
        # Attempt to interpret the witness as a Gram matrix of the bilinear form
        if not isinstance(witness, Matrix):
            witness = Matrix(witness)
            
        if not getattr(witness, 'is_square', False):
            neg_q = True
        elif not witness.is_symmetric():
            neg_q = True
        else:
            det_val = witness.det()
            if det_val == 0:
                neg_q = True
            elif isinstance(det_val, sympy.Expr) and sympy.simplify(det_val) == 0:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: V does not admit a unique orthogonal decomposition into a hyperbolic and an anisotropic space"
]

N_HYP = 0
NEG_Q_INDEX = 0