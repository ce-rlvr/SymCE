import sympy
from sympy import ZZ, QQ, igcd
from sympy.abc import x, y, z
from functools import reduce

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: I is not equal to R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif hasattr(witness, 'ring'):
            R = witness.ring
            I = witness
        elif isinstance(witness, (int, sympy.Integer)):
            R = sympy.ZZ
            I = witness
        elif isinstance(witness, list) and all(isinstance(val, (int, sympy.Integer)) for val in witness):
            R = sympy.ZZ
            I = witness
        else:
            R, I = None, None
    except Exception:
        R, I = None, None

    # H1: R is a commutative ring
    h1_ok = False
    try:
        if R in (sympy.ZZ, sympy.QQ):
            h1_ok = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1_ok = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            h1_ok = True
    except Exception:
        pass

    # H2: I is an ideal of R
    h2_ok = False
    try:
        if hasattr(I, 'ring') and I.ring == R:
            h2_ok = True
        elif R == sympy.ZZ:
            if isinstance(I, (int, sympy.Integer)):
                h2_ok = True
            elif isinstance(I, (list, tuple, set)) and all(isinstance(val, (int, sympy.Integer)) for val in I):
                h2_ok = True
        elif R == sympy.QQ:
            if isinstance(I, (int, sympy.Integer, sympy.Rational, float)):
                h2_ok = True
            elif isinstance(I, (list, tuple, set)) and all(isinstance(val, (int, sympy.Integer, sympy.Rational, float)) for val in I):
                h2_ok = True
    except Exception:
        pass

    # Q: I = R
    q_ok = None
    try:
        if hasattr(I, 'is_whole_ring'):
            q_ok = bool(I.is_whole_ring())
        elif R == sympy.ZZ:
            if isinstance(I, (int, sympy.Integer)):
                q_ok = (abs(int(I)) == 1)
            elif isinstance(I, (list, tuple, set)):
                if not I:
                    q_ok = False
                else:
                    g = reduce(igcd, [int(val) for val in I])
                    q_ok = (abs(g) == 1)
        elif R == sympy.QQ:
            if isinstance(I, (int, sympy.Integer, sympy.Rational, float)):
                q_ok = (I != 0)
            elif isinstance(I, (list, tuple, set)):
                q_ok = any(val != 0 for val in I)
        elif hasattr(I, 'contains') and hasattr(R, 'one'):
            q_ok = bool(I.contains(R.one))
    except Exception:
        pass

    if q_ok is None:
        neg_q_ok = False
    else:
        neg_q_ok = not q_ok

    return [h1_ok, h2_ok, neg_q_ok]