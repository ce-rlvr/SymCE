import sympy
from sympy import eye, zeros
from itertools import product

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_nonzero(diff):
    if diff == 0:
        return False
    diff_simp = sympy.simplify(diff)
    if diff_simp == 0:
        return False
    if diff_simp.is_number:
        try:
            return abs(complex(diff_simp)) > 1e-12
        except Exception:
            return True
    return True

def conditions(witness):
    try:
        U, V = witness
        if not isinstance(U, sympy.MatrixBase):
            U = sympy.Matrix(U)
        if not isinstance(V, sympy.MatrixBase):
            V = sympy.Matrix(V)
        if U.shape != V.shape or U.shape[0] != U.shape[1]:
            return [False, False]
        n = U.shape[0]
    except Exception:
        return [False, False]

    # H_1: For every integer k such that 1 <= k <= n, trace(U^k) == trace(V^k)
    h1_ok = True
    try:
        for k in range(1, n + 1):
            diff = (U**k).trace() - (V**k).trace()
            if is_nonzero(diff):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # neg_Q: U and V are NOT unitarily similar
    # We use Specht's theorem, checking traces of words in A and A* up to length 6.
    neg_q_ok = False
    try:
        U_adj = U.adjoint()
        V_adj = V.adjoint()
        
        are_similar = True
        for length in range(1, 7):
            for word in product([0, 1], repeat=length):
                U_prod = eye(n)
                V_prod = eye(n)
                for bit in word:
                    U_prod = U_prod * (U if bit == 0 else U_adj)
                    V_prod = V_prod * (V if bit == 0 else V_adj)
                diff = U_prod.trace() - V_prod.trace()
                if is_nonzero(diff):
                    are_similar = False
                    break
            if not are_similar:
                break
        
        neg_q_ok = not are_similar
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: For 1 <= k <= n, trace(U^k) == trace(V^k)",
    "¬Q: U and V are not unitarily similar"
]
N_HYP = 1
NEG_Q_INDEX = 1