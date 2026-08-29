import sympy
from sympy import eye, zeros, Matrix, S
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        P, z_val = witness
    except Exception:
        return [False, False]

    try:
        if isinstance(z_val, MatrixBase):
            h1 = False
        else:
            if z_val == 0 or z_val == 1:
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    try:
        if not isinstance(P, MatrixBase) or not P.is_square:
            neg_q = False
        else:
            I = eye(P.shape[0])
            RHS = (S(1)/z_val)*I + (S(1)/(z_val*(z_val-1)))*P
            try:
                LHS = (z_val*I - P).inv()
                diff = LHS - RHS
                is_zero = True
                for i in range(diff.rows):
                    for j in range(diff.cols):
                        val = diff[i, j]
                        if val != 0:
                            if hasattr(val, 'simplify'):
                                val = val.simplify()
                            if val != 0:
                                is_zero = False
                                break
                    if not is_zero:
                        break
                neg_q = not is_zero
            except Exception:
                # If zI - P is not invertible, the equality fails
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: z is a complex scalar such that z != 0 and z != 1",
    "¬Q: The resolvent matrix (zI - P)^{-1} is not equal to (1/z)I + (1/(z(z-1)))P"
]

N_HYP = 1
NEG_Q_INDEX = 1