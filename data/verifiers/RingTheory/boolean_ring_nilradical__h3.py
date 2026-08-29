import sympy
from sympy import Mod

# Top-level setup
Z2 = [Mod(0, 2), Mod(1, 2)]

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        else:
            R = Z2
            x = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a Boolean ring
    h1 = False
    elements = []
    try:
        for i, e in enumerate(R):
            if i > 100:
                break
            elements.append(e)
        else:
            n = len(elements)
            if n > 0:
                zeros = [z for z in elements if all(z + a == a and a + z == a for a in elements)]
                if len(zeros) == 1:
                    zero = zeros[0]
                    is_ring = True
                    for a in elements:
                        if a * a != a:
                            is_ring = False
                            break
                        if not any(a + b == zero and b + a == zero for b in elements):
                            is_ring = False
                            break
                        for b in elements:
                            if a + b not in elements or a * b not in elements:
                                is_ring = False
                                break
                            if a + b != b + a:
                                is_ring = False
                                break
                            for c in elements:
                                if (a + b) + c != a + (b + c):
                                    is_ring = False
                                    break
                                if (a * b) * c != a * (b * c):
                                    is_ring = False
                                    break
                                if a * (b + c) != a * b + a * c:
                                    is_ring = False
                                    break
                                if (a + b) * c != a * c + b * c:
                                    is_ring = False
                                    break
                            if not is_ring: break
                        if not is_ring: break
                    h1 = is_ring
    except Exception:
        h1 = False

    # H_2: x is an element of R
    h2 = False
    try:
        h2 = x in elements
    except Exception:
        h2 = False

    # neg_Q: x != 0
    neg_q = False
    try:
        zeros = [z for z in elements if all(z + a == a and a + z == a for a in elements)]
        if len(zeros) == 1:
            zero = zeros[0]
            neg_q = bool(x != zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: x is an element of R",
    "¬Q: x != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2