import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            S = witness.get('S')
            T = witness.get('T')
            if S is None or T is None:
                return [False, False, False]
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                S, T = witness
            elif len(witness) == 4:
                _, _, S, T = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: V and W are vector spaces over a field F
    try:
        h1 = isinstance(S, sp.MatrixBase) and isinstance(T, sp.MatrixBase)
    except Exception:
        h1 = False

    # H_2: S: V -> W and T: W -> V are linear transformations
    try:
        h2 = h1 and (S.shape[1] == T.shape[0]) and (S.shape[0] == T.shape[1])
    except Exception:
        h2 = False

    # ¬Q: The operator I_V - TS is invertible if and only if the operator I_W - ST is invertible (must fail)
    try:
        if h2:
            n = S.shape[1] # dim V
            m = S.shape[0] # dim W
            
            I_V = sp.eye(n)
            I_W = sp.eye(m)
            
            op_V = I_V - T * S
            op_W = I_W - S * T
            
            # Invertibility over a field is equivalent to a non-zero determinant
            inv_V = (op_V.det() != 0)
            inv_W = (op_W.det() != 0)
            
            # The conclusion is that they are either both invertible or both not invertible.
            # The negation is that one is invertible and the other is not.
            neg_q = bool(inv_V != inv_W)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: S: V -> W and T: W -> V are linear transformations",
    "¬Q: I_V - TS is invertible but I_W - ST is not, or vice versa"
]

N_HYP = 2
NEG_Q_INDEX = 2