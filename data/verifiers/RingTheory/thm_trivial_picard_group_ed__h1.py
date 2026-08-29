import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.domains import Domain

def conditions(witness) -> list[bool]:
    def check_euclidean(w):
        if hasattr(w, 'is_euclidean_domain'):
            val = w.is_euclidean_domain
            return val() if callable(val) else bool(val)
        if isinstance(w, int):
            # Known Euclidean quadratic fields Q(sqrt(d)) for squarefree d
            euclidean_d = {
                -11, -7, -3, -2, -1, 
                2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 22, 23, 29, 31, 33, 37, 38, 
                41, 43, 46, 47, 53, 57, 59, 61, 62, 67, 69, 71, 73, 77, 83, 86, 89, 93, 94, 97
            }
            return w in euclidean_d
        if isinstance(w, Domain):
            if w.is_Field or w == ZZ:
                return True
            if hasattr(w, 'is_PID') and w.is_PID:
                return True
        if isinstance(w, str):
            w_clean = w.replace(" ", "")
            if w_clean in ["Z", "Q", "R", "C"]:
                return True
            if w_clean.startswith("Q[") or w_clean.startswith("R[") or w_clean.startswith("C["):
                return True
            if w_clean.startswith("Z["):
                return False
        return False

    def check_picard_trivial(w):
        if hasattr(w, 'is_picard_group_trivial'):
            val = w.is_picard_group_trivial
            return val() if callable(val) else bool(val)
        if hasattr(w, 'picard_group'):
            val = w.picard_group
            group = val() if callable(val) else val
            if hasattr(group, 'is_trivial'):
                return group.is_trivial
            if hasattr(group, 'order'):
                return group.order() == 1
            return group == 1 or group == "trivial"
        if isinstance(w, int):
            # Quadratic fields with class number 1
            class_1_negative = {-163, -67, -43, -19, -11, -7, -3, -2, -1}
            class_1_positive = {
                2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 22, 23, 29, 31, 33, 37, 38, 
                41, 43, 46, 47, 53, 57, 59, 61, 62, 67, 69, 71, 73, 77, 83, 86, 89, 93, 94, 97
            }
            if w < 0:
                return w in class_1_negative
            if w > 0:
                return w in class_1_positive
        if isinstance(w, Domain):
            if w.is_Field or w == ZZ:
                return True
            if hasattr(w, 'is_PID') and w.is_PID:
                return True
        if isinstance(w, str):
            w_clean = w.replace(" ", "")
            if w_clean in ["Z", "Q", "R", "C"]:
                return True
            if w_clean.startswith("Q[") or w_clean.startswith("R[") or w_clean.startswith("C[") or w_clean.startswith("Z["):
                return True
        return False

    try:
        h1 = bool(check_euclidean(witness))
    except Exception:
        h1 = False

    try:
        neg_q = not bool(check_picard_trivial(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: The Picard group Pic(R) is not trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1