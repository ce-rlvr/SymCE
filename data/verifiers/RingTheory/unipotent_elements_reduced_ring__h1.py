import sympy
from sympy import MatrixBase, eye, zeros, simplify

# Setup standard linear algebra objects for potential matrix witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_matrix(m, Z):
    if m == Z:
        return True
    for e in m:
        if e == 0:
            continue
        try:
            if simplify(e) != 0:
                return False
        except Exception:
            return False
    return True

def is_zero_scalar(s):
    if s == 0:
        return True
    try:
        return simplify(s) == 0
    except Exception:
        return False

def conditions(witness):
    # H_1: u is a unipotent element (u - 1 is nilpotent)
    try:
        if isinstance(witness, MatrixBase):
            if witness.shape[0] != witness.shape[1]:
                h1_ok = False
            else:
                I = eye(witness.shape[0])
                Z = zeros(witness.shape[0], witness.shape[1])
                x = witness - I
                
                is_nilpotent = False
                curr = x
                for _ in range(30):
                    if is_zero_matrix(curr, Z):
                        is_nilpotent = True
                        break
                    curr = curr * x
                h1_ok = is_nilpotent
        else:
            I = 1
            x = witness - I
            
            is_nilpotent = False
            curr = x
            for _ in range(30):
                if is_zero_scalar(curr):
                    is_nilpotent = True
                    break
                curr = curr * x
            h1_ok = is_nilpotent
    except Exception:
        h1_ok = False

    # ¬Q: u is not the identity element
    try:
        if isinstance(witness, MatrixBase):
            I = eye(witness.shape[0])
            Z = zeros(witness.shape[0], witness.shape[1])
            if is_zero_matrix(witness - I, Z):
                neg_q_ok = False
            else:
                neg_q_ok = True
        else:
            I = 1
            if is_zero_scalar(witness - I):
                neg_q_ok = False
            else:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: u is a unipotent element (u - 1 is nilpotent)",
    "¬Q: u is not the identity element"
]

N_HYP = 1
NEG_Q_INDEX = 1