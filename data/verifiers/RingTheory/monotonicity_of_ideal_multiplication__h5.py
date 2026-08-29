import math
import sympy
from sympy import ZZ

Z = ZZ

def conditions(witness) -> list[bool]:
    def get_generator(gen):
        if isinstance(gen, (int, sympy.Integer)):
            return int(gen)
        elif isinstance(gen, (list, tuple, set)):
            g = 0
            for x in gen:
                g = math.gcd(g, int(x))
            return g
        else:
            raise ValueError("Not a valid generator")

    try:
        if isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                R, I, J, K = witness
            elif len(witness) == 3:
                R = "Z"
                I, J, K = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    try:
        h1 = (R in ("Z", "ZZ", ZZ, sympy.S.Integers))
    except Exception:
        h1 = False

    try:
        I_gen = get_generator(I)
        h2 = h1
    except Exception:
        h2 = False

    try:
        J_gen = get_generator(J)
        h3 = h1
    except Exception:
        h3 = False

    try:
        K_gen = get_generator(K)
        h4 = h1
    except Exception:
        h4 = False

    try:
        if h1 and h2 and h3 and h4:
            ik = I_gen * K_gen
            jk = J_gen * K_gen
            if jk == 0:
                is_subset = (ik == 0)
            else:
                is_subset = (ik % jk == 0)
            neg_q = not is_subset
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "H_4: K is an ideal of R",
    "¬Q: IK is not a subset of JK"
]

N_HYP = 4
NEG_Q_INDEX = 4