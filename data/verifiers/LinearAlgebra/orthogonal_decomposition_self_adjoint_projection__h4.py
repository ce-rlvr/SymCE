import sympy
from sympy import eye, zeros, Matrix
from sympy.matrices import MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        B, P = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: V is a vector space over a field F
    # We verify this by checking that B and P are square matrices of the same dimension,
    # which implicitly defines the vector space V = F^n.
    try:
        h1 = (isinstance(B, MatrixBase) and isinstance(P, MatrixBase) and 
              B.is_square and P.is_square and B.shape == P.shape)
    except Exception:
        h1 = False

    # H_2: B is a symmetric bilinear form on V
    try:
        if h1:
            h2 = all(sympy.simplify(B[i, j] - B[j, i]) == 0 
                     for i in range(B.shape[0]) for j in range(B.shape[1]))
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: P is a linear projection operator on V, satisfying P^2 = P
    try:
        if h1:
            P_diff = P * P - P
            h3 = all(sympy.simplify(c) == 0 for c in P_diff)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: V is NOT the orthogonal direct sum of the image of P and the kernel of P
    # Since P is a projection, V is always the direct sum of Im(P) and Ker(P).
    # The sum is orthogonal iff Im(P) is orthogonal to Ker(P) with respect to B.
    # This means for all u, v in V, B(P*u, (I - P)*v) = 0, which is equivalent to P^T * B * (I - P) == 0.
    # The conclusion fails (¬Q is True) if this matrix is NOT zero.
    try:
        if h1:
            I = eye(B.shape[0])
            ortho_matrix = P.T * B * (I - P)
            neg_q = not all(sympy.simplify(c) == 0 for c in ortho_matrix)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: B is a symmetric bilinear form on V",
    "H_3: P is a linear projection operator on V, satisfying P^2 = P",
    "¬Q: V is not the orthogonal direct sum of the image of P and the kernel of P"
]

N_HYP = 3
NEG_Q_INDEX = 3