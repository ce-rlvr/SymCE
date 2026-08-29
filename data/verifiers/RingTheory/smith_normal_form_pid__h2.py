import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Standard domains for witness construction
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, A) where R is a domain and A is a matrix.
    The dropped hypothesis from the true theorem is that A must be a matrix over R.
    """
    try:
        R, A = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a principal ideal domain
    try:
        h1 = bool(R.is_PID)
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion fails at the witness
    # The conclusion states there exist P, Q in GL(R) such that PAQ is a diagonal matrix
    # with diagonal entries d_i in R satisfying d_i | d_{i+1}.
    # If A has entries that do not belong to R, then no such P, Q over R can exist,
    # because P, Q in GL(R) implies A = P^{-1} D Q^{-1} would have to be a matrix over R.
    try:
        if not (hasattr(A, 'is_Matrix') and A.is_Matrix):
            neg_q = True
        else:
            is_over_R = True
            for e in A:
                if e not in R:
                    is_over_R = False
                    break
            neg_q = not is_over_R
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: There do not exist P, Q in GL(R) such that PAQ is a diagonal matrix with d_i | d_{i+1}"
]

N_HYP = 1
NEG_Q_INDEX = 1