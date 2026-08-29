import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
            K = witness.get('K')
        elif isinstance(witness, tuple) and len(witness) == 4:
            R, I, J, K = witness
        else:
            R, I, J, K = witness.R, witness.I, witness.J, witness.K
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    try:
        if R in (sympy.ZZ, sympy.QQ):
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: I is an invertible ideal
    try:
        if hasattr(I, 'is_invertible'):
            h2 = bool(I.is_invertible() if callable(I.is_invertible) else I.is_invertible)
        else:
            if hasattr(I, 'is_zero'):
                h2 = not I.is_zero
            else:
                h2 = (I != 0)
    except Exception:
        h2 = False

    # H3: IJ = IK
    try:
        if R == sympy.ZZ and isinstance(I, (int, sympy.Integer)) and isinstance(J, (int, sympy.Integer)) and isinstance(K, (int, sympy.Integer)):
            h3 = abs(int(I * J)) == abs(int(I * K))
        else:
            h3 = bool(I * J == I * K)
            if not h3 and hasattr(R, 'ideal'):
                h3 = bool(R.ideal(I * J) == R.ideal(I * K))
    except Exception:
        h3 = False

    # neg_Q: J != K
    try:
        neg_q = bool(J != K)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an invertible ideal",
    "H_3: IJ = IK",
    "¬Q: J != K"
]

N_HYP = 3
NEG_Q_INDEX = 3