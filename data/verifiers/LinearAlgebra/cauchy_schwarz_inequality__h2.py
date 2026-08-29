import sympy

# Top-level setup for standard objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is an inner product space over the field of real or complex numbers",
    "¬Q: |<u, v>| > ||u|| ||v||"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false Cauchy-Schwarz conjecture.
    The dropped hypothesis is that the inner product is positive-definite.
    A valid counterexample will provide an indefinite inner product metric A, and vectors u, v.
    """
    try:
        if len(witness) == 3:
            A, u, v = witness
            A = sympy.Matrix(A)
            u = sympy.Matrix(u)
            v = sympy.Matrix(v)
        elif len(witness) == 2:
            u, v = witness
            u = sympy.Matrix(u)
            v = sympy.Matrix(v)
            A = sympy.eye(u.shape[0])
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: V is an inner product space over R or C
    # We check if A defines a valid non-degenerate Hermitian form
    try:
        if A.shape[0] != A.shape[1]:
            h1 = False
        elif A.shape[0] != u.shape[0] or A.shape[0] != v.shape[0]:
            h1 = False
        elif u.shape[1] != 1 or v.shape[1] != 1:
            h1 = False
        elif A != A.H:
            h1 = False
        elif A.det() == 0:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: The conclusion |<u, v>| <= ||u|| ||v|| FAILS
    try:
        inner = (u.H * A * v)[0]
        norm_u_sq = (u.H * A * u)[0]
        norm_v_sq = (v.H * A * v)[0]
        
        norm_u = sympy.sqrt(norm_u_sq)
        norm_v = sympy.sqrt(norm_v_sq)
        
        lhs = sympy.Abs(inner)
        rhs = norm_u * norm_v
        
        try:
            rel = lhs <= rhs
            if rel == True:
                holds = True
            elif rel == False:
                holds = False
            else:
                holds = bool(sympy.simplify(rel))
        except TypeError:
            # TypeError occurs when comparing complex numbers (e.g., imaginary norms),
            # which means the inequality is mathematically undefined and thus fails.
            holds = False
            
        neg_q = not holds
    except Exception:
        neg_q = False

    return [h1, neg_q]