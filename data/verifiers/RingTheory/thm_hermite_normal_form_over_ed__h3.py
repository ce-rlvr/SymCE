import sympy
from sympy import Matrix, eye, zeros, ZZ, QQ, S
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (R, A) where R is a domain and A is a matrix.
    """
    try:
        R, A = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is an integral domain
    try:
        h1 = False
        if R in [ZZ, QQ, S.Integers, S.Rationals, S.Reals, S.Complexes]:
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'is_domain') and R.is_domain:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            h1 = True
    except Exception:
        h1 = False

    # H_2: R is a Euclidean domain
    try:
        h2 = False
        if R in [ZZ, S.Integers]:
            h2 = True
        elif R in [QQ, S.Rationals, S.Reals, S.Complexes]:
            h2 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h2 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            # A polynomial ring over a field in one variable is a Euclidean domain
            if R.domain.is_Field and len(R.symbols) == 1:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist an invertible m x m matrix U over R such that UA is in Hermite normal form.
    # Mathematically, over any Euclidean domain, every matrix OVER THAT DOMAIN has a Hermite normal form.
    # The only way such an invertible matrix U over R does not exist is if the matrix A itself 
    # is not a matrix over R (e.g., it contains fractional entries not in R).
    try:
        if not isinstance(A, Matrix):
            try:
                A = Matrix(A)
            except Exception:
                pass
                
        if not isinstance(A, Matrix):
            neg_q = False
        else:
            is_over_R = True
            for e in A:
                if e not in R:
                    is_over_R = False
                    break
            
            # If A is over R, HNF always exists, so the conclusion holds (neg_Q is False).
            # If A is not over R, HNF over R cannot exist, so the conclusion fails (neg_Q is True).
            neg_q = not is_over_R
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R is a Euclidean domain",
    "¬Q: There does not exist an invertible matrix U over R such that UA is in Hermite normal form"
]

N_HYP = 2
NEG_Q_INDEX = 2