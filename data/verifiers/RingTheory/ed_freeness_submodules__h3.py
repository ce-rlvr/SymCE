import sympy
from sympy import ZZ, QQ

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness):
    try:
        R, F, M, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a Euclidean domain
    try:
        h1 = False
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
    except Exception:
        h1 = False

    # H_2: F is a free R-module of finite rank n
    try:
        h2 = False
        if hasattr(F, 'ring') and F.ring == R and isinstance(n, int):
            if F.__class__.__name__ == 'FreeModule':
                if hasattr(F, 'rank') and F.rank == n:
                    h2 = True
            elif F.__class__.__name__ == 'SubModule':
                try:
                    gens = F.gens
                    mat = sympy.Matrix([list(g) for g in gens])
                    if mat.rank() == n:
                        h2 = True
                except Exception:
                    pass
    except Exception:
        h2 = False

    # ¬Q: M is not a free R-module of rank k <= n
    try:
        q = False
        if hasattr(M, 'ring') and M.ring == R:
            if M.__class__.__name__ == 'FreeModule':
                if hasattr(M, 'rank') and M.rank <= n:
                    q = True
            elif M.__class__.__name__ == 'SubModule':
                try:
                    gens = M.gens
                    mat = sympy.Matrix([list(g) for g in gens])
                    if mat.rank() <= n:
                        q = True
                except Exception:
                    pass
        neg_q = not q
    except Exception:
        # If M lacks module attributes, it is not a free R-module of rank <= n
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: F is a free R-module of finite rank n",
    "¬Q: M is not a free R-module of rank k <= n"
]

N_HYP = 2
NEG_Q_INDEX = 2