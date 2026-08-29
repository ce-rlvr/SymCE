import sympy
from sympy import Matrix, eye, zeros, poly
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Expected witness: (T, W, p)
    - T: sympy Matrix representing the linear operator on V
    - W: sympy Matrix whose columns span the subspace W of V
    - p: sympy expression in x representing the polynomial
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        T, W, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: V is a vector space (implied by T and W dimensions)
    try:
        h1 = isinstance(T, Matrix) and isinstance(W, Matrix) and T.shape[0] == W.shape[0]
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V
    try:
        h2 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h2 = False

    # H_3: p(x) is a polynomial such that p(T)v = 0 for all v in V
    try:
        poly_obj = poly(p, x)
        if poly_obj is None:
            h3 = False
        else:
            coeffs = poly_obj.all_coeffs()
            n = T.shape[0]
            result = zeros(n, n)
            T_pow = eye(n)
            # all_coeffs() returns coefficients from highest degree to lowest
            for c in coeffs[::-1]:
                result += c * T_pow
                T_pow = T_pow * T
            h3 = (result == zeros(n, n))
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails.
    # The conclusion states that the induced quotient operator T_bar on V/W satisfies p(T_bar)v_bar = 0.
    # This presupposes that T_bar is well-defined, which requires W to be T-invariant.
    # If W is T-invariant, p(T_bar) = 0 is always true because p(T) = 0.
    # Therefore, the conclusion fails if and only if W is NOT T-invariant.
    try:
        rank_W = W.rank()
        TW = T * W
        W_TW = W.row_join(TW)
        rank_W_TW = W_TW.rank()
        
        # W is T-invariant iff rank(W) == rank([W | T*W])
        is_invariant = (rank_W == rank_W_TW)
        neg_q = not is_invariant
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space (and W is a subspace of V)",
    "H_2: T is a linear operator on V",
    "H_3: p(x) is a polynomial such that p(T)v = 0 for all v in V",
    "¬Q: The induced quotient operator is not well-defined (W is not T-invariant)"
]

N_HYP = 3
NEG_Q_INDEX = 3