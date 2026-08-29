import sympy
from sympy import Matrix, eye, zeros
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion.
    
    The dropped hypothesis from the true theorem was "Let A be a matrix over R".
    Without it, the witness is a tuple (R, A) where A might not be a matrix over R.
    """
    try:
        # The witness is expected to be a tuple (Ring, Matrix)
        R, A = witness
    except Exception:
        return [False, False]
        
    # H_1: Let R be a Euclidean domain
    try:
        # In SymPy, all implemented PIDs are Euclidean domains (e.g., ZZ, QQ, F[x])
        h1 = hasattr(R, 'is_PID') and R.is_PID
    except Exception:
        h1 = False
        
    # neg_Q: Conclusion fails
    # The conclusion states there exist U, V in GL(R) such that UAV is a diagonal matrix 
    # where each diagonal entry divides the subsequent one (Smith Normal Form over R).
    # If A is not a matrix, or if A has elements that do not belong to R, 
    # it cannot be diagonalized over R in this manner.
    try:
        if not isinstance(A, sympy.MatrixBase):
            neg_q = True
        else:
            is_over_R = True
            for elem in A:
                try:
                    # Attempt to coerce the element into the domain R
                    val = R.from_sympy(sympy.sympify(elem))
                    if val is None:
                        is_over_R = False
                        break
                except Exception:
                    is_over_R = False
                    break
            
            # If A is over R, the Smith Normal Form always exists mathematically.
            # If A is not over R, the conclusion fails.
            neg_q = not is_over_R
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: There do not exist invertible matrices U and V over R such that UAV is in Smith Normal Form"
]

N_HYP = 1
NEG_Q_INDEX = 1