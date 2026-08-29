import sympy
from sympy import eye, zeros, MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1_ok = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            P = witness
            I = eye(P.shape[0])
            I_minus_P = I - P
            
            sv_P = P.singular_values()
            sv_I_P = I_minus_P.singular_values()
            
            gt1_P = []
            for s in sv_P:
                val = float(s.evalf())
                if val > 1 + 1e-7:
                    gt1_P.append(val)
            gt1_P.sort()
            
            gt1_I_P = []
            for s in sv_I_P:
                val = float(s.evalf())
                if val > 1 + 1e-7:
                    gt1_I_P.append(val)
            gt1_I_P.sort()
            
            if len(gt1_P) != len(gt1_I_P):
                neg_q_ok = True
            else:
                neg_q_ok = False
                for s1, s2 in zip(gt1_P, gt1_I_P):
                    if abs(s1 - s2) > 1e-5:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a square matrix",
    "¬Q: The singular values of P strictly > 1 are NOT exactly the same as those of I - P"
]

N_HYP = 1
NEG_Q_INDEX = 1