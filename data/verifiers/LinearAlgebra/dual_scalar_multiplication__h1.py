import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any scalar λ and linear operator T(v) = λv,
    the dual transformation T* is defined by T*(f) = λf.
    This fails if the field is non-commutative (e.g., skew-field or matrix ring)
    or if the space is an inner product space where T* is the adjoint (conjugate transpose).
    """
    # Extract lam from witness
    if isinstance(witness, dict):
        lam = witness.get('lam', witness)
    else:
        lam = witness

    # H1: λ is a scalar in F
    try:
        valid_types = (int, float, complex, sp.Expr, sp.MatrixBase)
        if isinstance(lam, valid_types):
            h1 = True
        elif not isinstance(lam, (str, list, tuple, dict, set)) and hasattr(lam, '__mul__') and hasattr(lam, '__add__'):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: T: V -> V is a linear operator defined by T(v) = λv for all v in V
    h2 = True
    try:
        if isinstance(witness, dict) and 'T' in witness:
            T = witness['T']
            if hasattr(T, 'shape'):
                I = sp.eye(T.shape[0])
                if T != lam * I:
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: The dual transformation T*: V* -> V* is NOT defined by T*(f) = λf for all f in V*
    
    # Method 1: Non-commutative scalar (f(v) * lam != lam * f(v))
    diff1 = False
    try:
        if isinstance(lam, sp.MatrixBase):
            if lam.shape[0] == lam.shape[1]:
                n = lam.shape[0]
                B = sp.MatrixSymbol('B', n, n)
                expr_mat = sp.Matrix(lam * B - B * lam)
                diff1 = not expr_mat.is_zero_matrix
            else:
                diff1 = False
        else:
            f_v = sp.Symbol('f_v', commutative=False)
            expr = lam * f_v - f_v * lam
            if hasattr(expr, 'is_zero_matrix') and expr.is_zero_matrix:
                diff1 = False
            elif expr == 0:
                diff1 = False
            else:
                diff1 = True
    except Exception:
        diff1 = False

    # Method 2: Inner product space adjoint (T*(v) = conjugate(lam) * v)
    diff2 = False
    try:
        if isinstance(lam, sp.MatrixBase):
            adj_lam = lam.adjoint()
            if adj_lam != lam:
                diff2 = True
        else:
            conj_lam = sp.conjugate(lam)
            if isinstance(lam, sp.Expr):
                diff_expr = sp.simplify(conj_lam - lam)
                if diff_expr.is_zero is False:
                    diff2 = True
            else:
                if conj_lam != lam:
                    diff2 = True
    except Exception:
        diff2 = False

    # Method 3: Witness explicitly provides a counterexample T_star
    diff3 = False
    try:
        if isinstance(witness, dict) and 'T_star' in witness:
            T_star = witness['T_star']
            if hasattr(T_star, 'shape'):
                I = sp.eye(T_star.shape[0])
                if T_star != lam * I:
                    diff3 = True
    except Exception:
        diff3 = False

    try:
        neg_q = bool(diff1 or diff2 or diff3)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: λ is a scalar in F",
    "H_2: T: V -> V is a linear operator defined by T(v) = λv for all v in V",
    "¬Q: The dual transformation T*: V* -> V* is NOT defined by T*(f) = λf for all f in V*"
]

N_HYP = 2
NEG_Q_INDEX = 2