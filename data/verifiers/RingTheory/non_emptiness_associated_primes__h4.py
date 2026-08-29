import sympy
from sympy import S, eye, zeros

# Top-level setup
ZZ = S.Integers
QQ = S.Rationals
Z = ZZ
Q = QQ

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_module(M):
    try:
        if M == 0 or M == [0] or M == (0,) or M == []:
            return True
    except Exception:
        pass
    try:
        if isinstance(M, str):
            s = M.strip().lower()
            if s in ("0", "{0}", "[0]", "0 module", "zero module", "zero", "()"):
                return True
    except Exception:
        pass
    try:
        if hasattr(M, 'is_zero_matrix') and M.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if hasattr(M, 'is_zero') and M.is_zero:
            return True
    except Exception:
        pass
    try:
        if hasattr(M, 'is_Zero') and M.is_Zero:
            return True
    except Exception:
        pass
    try:
        if isinstance(M, (list, tuple)) and len(M) > 0 and all(is_zero_module(x) for x in M):
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        elif isinstance(witness, dict):
            R = witness.get("R", ZZ)
            M = witness.get("M", 0)
        else:
            R = ZZ
            M = witness

        # H_1: R is a commutative ring
        try:
            if R in (ZZ, QQ):
                h1 = True
            elif isinstance(R, str):
                h1 = True
            else:
                h1 = bool(getattr(R, 'is_commutative', True))
        except Exception:
            h1 = False

        # H_2: R is a Noetherian ring
        try:
            if R in (ZZ, QQ):
                h2 = True
            elif isinstance(R, str):
                h2 = True
            else:
                h2 = bool(getattr(R, 'is_noetherian', True))
        except Exception:
            h2 = False

        # H_3: M is a finitely generated R-module
        try:
            if is_zero_module(M):
                h3 = True
            elif hasattr(M, 'is_Matrix') or isinstance(M, (list, tuple)):
                h3 = True
            else:
                h3 = False
        except Exception:
            h3 = False

        # neg_Q: Ass_R(M) is empty
        try:
            neg_q = is_zero_module(M)
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a Noetherian ring",
    "H_3: M is a finitely generated R-module",
    "¬Q: Ass_R(M) is empty"
]

N_HYP = 3
NEG_Q_INDEX = 3