import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: B is a k x k matrix (and J is of the same size)
    try:
        if isinstance(witness, dict):
            J_raw = witness['J']
            B_raw = witness['B']
        else:
            J_raw, B_raw = witness
        J = Matrix(J_raw)
        B = Matrix(B_raw)
        h1 = (len(J.shape) == 2 and len(B.shape) == 2 and 
              J.shape[0] == J.shape[1] and 
              B.shape[0] == B.shape[1] and 
              J.shape == B.shape)
    except Exception:
        h1 = False

    # H_2: JB = BJ
    try:
        if isinstance(witness, dict):
            J_raw = witness['J']
            B_raw = witness['B']
        else:
            J_raw, B_raw = witness
        J = Matrix(J_raw)
        B = Matrix(B_raw)
        if J.shape != B.shape or J.shape[0] != J.shape[1]:
            h2 = False
        else:
            k = J.shape[0]
            diff = J * B - B * J
            h2 = all(sympy.expand(diff[i, j]) == 0 for i in range(k) for j in range(k))
    except Exception:
        h2 = False

    # ¬Q: B is NOT an upper triangular Toeplitz matrix
    try:
        if isinstance(witness, dict):
            B_raw = witness['B']
        else:
            _, B_raw = witness
        B = Matrix(B_raw)
        
        if len(B.shape) != 2 or B.shape[0] != B.shape[1]:
            neg_q = True
        else:
            k = B.shape[0]
            is_utt = True
            
            # Check if upper triangular
            for i in range(k):
                for j in range(i):
                    if sympy.expand(B[i, j]) != 0:
                        is_utt = False
                        break
                if not is_utt:
                    break
            
            # Check if Toeplitz (constant diagonals)
            if is_utt:
                for i in range(k - 1):
                    for j in range(k - 1):
                        if sympy.expand(B[i, j] - B[i+1, j+1]) != 0:
                            is_utt = False
                            break
                    if not is_utt:
                        break
                        
            neg_q = not is_utt
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: B is a k x k matrix (and J is of the same size)",
    "H_2: JB = BJ",
    "¬Q: B is not an upper triangular Toeplitz matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2