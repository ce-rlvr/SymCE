import sympy
from sympy import ZZ, QQ, Symbol

# Top-level setup for potential witness expressions
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a ring and N is a submodule of M, then N is an Artinian R-module."
    
    Expected witness format: a tuple (R, M, N)
    """
    try:
        R, M, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a ring
    h1 = False
    try:
        if hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
        elif R in [ZZ, QQ]:
            h1 = True
    except Exception:
        pass
        
    # H2: N is a submodule of M
    h2 = False
    try:
        if M == R and N == R:
            h2 = True
        elif R == ZZ and M == QQ and N == ZZ:
            h2 = True
        elif R == ZZ and M == ZZ and isinstance(N, int):
            h2 = True
        elif hasattr(N, 'is_submodule') and N.is_submodule(M):
            h2 = True
    except Exception:
        pass
        
    # neg_Q: N is not an Artinian R-module
    neg_q = False
    try:
        if R == ZZ:
            if N == ZZ:
                neg_q = True
            elif isinstance(N, int) and N != 0:
                neg_q = True
            elif hasattr(N, 'rank'):
                rank = N.rank() if callable(N.rank) else N.rank
                if rank > 0:
                    neg_q = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            # E.g., Polynomial rings like QQ[x] are not Artinian
            if N == R:
                neg_q = True
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: N is a submodule of M",
    "¬Q: N is not an Artinian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2