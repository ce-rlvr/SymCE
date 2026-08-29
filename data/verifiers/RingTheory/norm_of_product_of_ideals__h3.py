import sympy

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    try:
        if isinstance(witness, dict):
            K = witness.get("K", None)
            O_K = witness.get("O_K", None)
            I = witness.get("I", None)
            J = witness.get("J", None)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                K, O_K, I, J = witness
            elif len(witness) == 2:
                K, O_K = QQ, ZZ
                I, J = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: K is a number field
    try:
        h1 = False
        if isinstance(K, str):
            if K.strip().upper() in ["Q", "QQ", "RATIONALS", "RATIONALFIELD", "RATIONALFIELD()"]:
                h1 = True
        elif K in [sympy.S.Rationals, QQ]:
            h1 = True
    except Exception:
        h1 = False

    # H2: O_K is the ring of integers of K
    try:
        h2 = False
        if isinstance(O_K, str):
            if O_K.strip().upper() in ["Z", "ZZ", "INTEGERS", "INTEGERRING", "INTEGERRING()"]:
                h2 = True
        elif O_K in [sympy.S.Integers, ZZ]:
            h2 = True
    except Exception:
        h2 = False

    # H3: J is a non-zero ideal of O_K
    try:
        if isinstance(J, (int, sympy.Integer)):
            h3 = bool(J > 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: N(IJ) != N(I)N(J)
    # The conclusion fails when I is an element of O_K with a negative field norm.
    # In this case, the ideal norm of IJ is positive, but N(I)N(J) is negative.
    try:
        if isinstance(I, (int, sympy.Integer)) and isinstance(J, (int, sympy.Integer)):
            N_IJ = abs(I * J)
            N_I = I
            N_J = J
            neg_q = bool(N_IJ != N_I * N_J)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a number field",
    "H_2: O_K is the ring of integers of K",
    "H_3: J is a non-zero ideal of O_K",
    "¬Q: N(IJ) != N(I)N(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3