import sympy
from sympy import Matrix, I, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness can be a tuple (B, P1, P2) where B is the bilinear form matrix,
        # and P1, P2 are two invertible change-of-basis matrices.
        # Alternatively, if only B is provided and it's diagonal, we try to auto-generate P1 and P2.
        if isinstance(witness, tuple) and len(witness) == 3:
            B, P1, P2 = witness
            B = Matrix(B)
            P1 = Matrix(P1)
            P2 = Matrix(P2)
        else:
            B = Matrix(witness)
            P1 = None
            P2 = None
            
            # Auto-generate P1, P2 if B is diagonal and has a non-zero entry
            if B.is_square and B.is_diagonal() and any(B[i, i] != 0 for i in range(B.shape[0])):
                P1 = eye(B.shape[0])
                P2 = eye(B.shape[0])
                for i in range(B.shape[0]):
                    if B[i, i] != 0:
                        P2[i, i] = I  # Multiply one basis vector by the imaginary unit
                        break
    except Exception:
        return [False, False]

    # H_1: B is a symmetric bilinear form on V
    try:
        h1 = bool(B.is_square and B.is_symmetric())
    except Exception:
        h1 = False

    # neg_Q: The number of positive, negative, and zero diagonal entries in any diagonal 
    # matrix representation of B is NOT independent of the choice of orthogonal basis.
    try:
        neg_q = False
        if P1 is not None and P2 is not None:
            if P1.shape == B.shape and P2.shape == B.shape:
                det1 = sympy.expand(P1.det())
                det2 = sympy.expand(P2.det())
                if det1 != 0 and det2 != 0:
                    # P^T B P is the matrix representation of B in the new basis
                    D1 = P1.T * B * P1
                    D2 = P2.T * B * P2
                    
                    # An orthogonal basis for B means the matrix representation is diagonal
                    if D1.is_diagonal() and D2.is_diagonal():
                        def get_signature(D):
                            pos = 0
                            neg = 0
                            zero = 0
                            for i in range(D.shape[0]):
                                val = sympy.expand(D[i, i])
                                if val.is_positive:
                                    pos += 1
                                elif val.is_negative:
                                    neg += 1
                                elif val.is_zero:
                                    zero += 1
                            return (pos, neg, zero)
                        
                        sig1 = get_signature(D1)
                        sig2 = get_signature(D2)
                        
                        # If the signatures are different, the conclusion fails (neg_Q is True)
                        if sig1 != sig2:
                            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: B is a symmetric bilinear form on V",
    "¬Q: The number of positive, negative, and zero diagonal entries is not independent of the choice of orthogonal basis"
]

N_HYP = 1
NEG_Q_INDEX = 1