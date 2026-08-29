import sympy
from sympy.polys.domains import ZZ, QQ, FF
from sympy.abc import x, y

# Setup common ring domains for witness expressions
ZZ_x = ZZ[x]
QQ_x = QQ[x]
ZZ_x_y = ZZ[x, y]
QQ_x_y = QQ[x, y]
F2 = FF(2)
F3 = FF(3)
F2_x = F2[x]
F3_x = F3[x]

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple of two SymPy domains: (R1, R2)
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        R1, R2 = witness
    except Exception:
        return [False, False]

    # H_1: R_1 is a principal ideal domain
    try:
        h1 = bool(R1.is_PID)
    except Exception:
        h1 = False

    # ¬Q: R_1 \times R_2 is NOT a principal ideal ring
    try:
        # A direct product of rings R1 x R2 is a PIR if and only if both R1 and R2 are PIRs.
        # Since SymPy domains are integral domains, they are PIRs if and only if they are PIDs.
        r1_is_pir = bool(R1.is_PID)
        r2_is_pir = bool(R2.is_PID)
        is_pir = r1_is_pir and r2_is_pir
        neg_q = not is_pir
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R_1 is a principal ideal domain",
    "¬Q: R_1 \\times R_2 is not a principal ideal ring"
]

N_HYP = 1
NEG_Q_INDEX = 1