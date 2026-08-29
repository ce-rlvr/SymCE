import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_zero_mat(m):
    try:
        if hasattr(m, 'is_zero_matrix') and m.is_zero_matrix:
            return True
        simp = sp.simplify(m)
        if hasattr(simp, 'is_zero_matrix') and simp.is_zero_matrix:
            return True
        if hasattr(simp, 'as_explicit'):
            return simp.as_explicit().is_zero_matrix
        if hasattr(m, 'shape'):
            return bool(simp == sp.zeros(*m.shape))
        return bool(simp == 0)
    except Exception:
        return False

def conditions(witness):
    P = witness
    A = None
    p_norm = 2

    if isinstance(witness, tuple) and len(witness) == 2:
        P, arg = witness
        if isinstance(arg, sp.MatrixBase):
            A = arg
        else:
            p_norm = arg

    # H_1: V is a finite-dimensional inner product space
    try:
        if hasattr(P, 'is_square'):
            h1 = P.is_square
            if A is not None:
                h1 = h1 and A.is_square and P.shape == A.shape
        elif hasattr(P, 'shape'):
            h1 = P.shape[0] == P.shape[1]
            if A is not None:
                h1 = h1 and A.shape[0] == A.shape[1] and P.shape == A.shape
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: P^2 = P
    try:
        h2 = is_zero_mat(P**2 - P)
    except Exception:
        h2 = False

    # H_3: P = P^*
    try:
        if A is not None:
            # Self-adjoint with respect to inner product matrix A: A*P = P^H*A
            h3 = is_zero_mat(A * P - P.H * A)
        else:
            if hasattr(P, 'H'):
                h3 = is_zero_mat(P - P.H)
            elif hasattr(P, 'adjoint'):
                h3 = is_zero_mat(P - P.adjoint())
            else:
                h3 = False
    except Exception:
        h3 = False

    # H_4: P \neq 0
    try:
        h4 = not is_zero_mat(P)
    except Exception:
        h4 = False

    # ¬Q: \|P\| \neq 1
    try:
        if hasattr(P, 'norm'):
            try:
                n = P.norm(p_norm)
            except Exception:
                n = P.norm()
        else:
            n = None
            
        if n is not None:
            diff = sp.simplify(n - 1)
            neg_q = bool(diff != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: P^2 = P",
    "H_3: P = P^*",
    "H_4: P \\neq 0",
    "¬Q: \\|P\\| \\neq 1"
]

N_HYP = 4
NEG_Q_INDEX = 4