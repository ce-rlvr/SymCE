import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # H_1: The scalar 1 is not an eigenvalue of U
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square:
            h1_ok = False
        else:
            n = witness.shape[0]
            I = sympy.eye(n)
            h1_ok = bool((I - witness).det() != 0)
    except Exception:
        h1_ok = False

    # ¬Q: (I - U)^{-1} + (I - U^*)^{-1} != I
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square:
            neg_q_ok = False
        else:
            n = witness.shape[0]
            I = sympy.eye(n)
            U_star = witness.H
            term1 = (I - witness).inv()
            term2 = (I - U_star).inv()
            diff = term1 + term2 - I
            
            is_zero = True
            for i in range(n):
                for j in range(n):
                    if sympy.simplify(diff[i, j]) != 0:
                        is_zero = False
                        break
                if not is_zero:
                    break
            neg_q_ok = not is_zero
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The scalar 1 is not an eigenvalue of U",
    "¬Q: (I - U)^{-1} + (I - U^*)^{-1} != I"
]

N_HYP = 1
NEG_Q_INDEX = 1