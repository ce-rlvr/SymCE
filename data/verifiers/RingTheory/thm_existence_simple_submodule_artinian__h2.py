import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
M0 = [0]

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a right Artinian ring, then M contains a simple R-submodule."
    
    The dropped hypothesis is that M is a non-zero module.
    A valid counterexample is any right Artinian ring R and the zero module M = 0.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            # If the witness is just the module, assume R is Z2 (which is Artinian)
            R = Z2
            M = witness
    except Exception:
        return [False, False]
    
    # H_1: R is a right Artinian ring
    try:
        h1 = False
        if isinstance(R, int) and R > 0:
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif type(R).__name__ in ['GaloisField', 'FiniteField']:
            h1 = True
        elif R in ['Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z8', 'Z9', 'QQ', 'RR', 'CC']:
            h1 = True
    except Exception:
        h1 = False
        
    # ¬Q: M does not contain a simple R-submodule
    # This is true if and only if M is the zero module.
    try:
        neg_q = False
        if isinstance(M, (int, str)) and M in [0, "0", "M0", "zero"]:
            neg_q = True
        elif isinstance(M, (list, tuple, set)) and (len(M) == 0 or all(x == 0 for x in M)):
            neg_q = True
        elif hasattr(M, 'is_zero_matrix') and M.is_zero_matrix:
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: M does not contain a simple R-submodule"
]

N_HYP = 1
NEG_Q_INDEX = 1