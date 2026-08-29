import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    try:
        if isinstance(witness, dict):
            P = witness.get('P')
            S = witness.get('S')
            A = witness.get('A')
            if A is None and P is not None and S is not None:
                A = P * S
            return P, S, A
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                return witness[0], witness[1], witness[2]
            elif len(witness) == 2:
                return witness[0], witness[1], witness[0] * witness[1]
    except Exception:
        pass
    return None, None, None

def conditions(witness) -> list[bool]:
    P, S, A = parse_witness(witness)
    
    # H_1: P is an n x n real positive definite matrix
    h1_ok = False
    try:
        if P is not None and hasattr(P, 'is_square') and P.is_square:
            is_real = True
            for val in P:
                if val.is_real is False or val.has(sympy.I):
                    is_real = False
                    break
            if is_real and P.is_symmetric():
                pd = True
                for i in range(1, P.rows + 1):
                    if P[:i, :i].det() <= 0:
                        pd = False
                        break
                h1_ok = pd
    except Exception:
        h1_ok = False

    # H_2: A = PS is the product of P and S
    h2_ok = False
    try:
        if P is not None and S is not None and A is not None:
            if P.cols == S.rows:
                h2_ok = bool(A == P * S)
    except Exception:
        h2_ok = False

    # neg_Q: A is not diagonalizable over the complex numbers
    neg_q_ok = False
    try:
        if A is not None and hasattr(A, 'is_square') and A.is_square:
            neg_q_ok = not A.is_diagonalizable()
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is an n x n real positive definite matrix",
    "H_2: A = PS is the product of P and S",
    "¬Q: A is not diagonalizable over the complex numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2