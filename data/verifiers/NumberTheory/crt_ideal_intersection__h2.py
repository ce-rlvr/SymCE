import math
import sympy

def extract_m1_m2(witness):
    if isinstance(witness, dict):
        return witness['m1'], witness['m2']
    elif hasattr(witness, 'm1') and hasattr(witness, 'm2'):
        return witness.m1, witness.m2
    else:
        return witness[0], witness[1]

def conditions(witness) -> list[bool]:
    try:
        m1, m2 = extract_m1_m2(witness)
        h1 = isinstance(m1, int) and isinstance(m2, int) and m1 > 0 and m2 > 0
    except Exception:
        h1 = False

    # H2 and H3 are definitional given m1 and m2
    h2 = h1
    h3 = h1

    try:
        m1, m2 = extract_m1_m2(witness)
        if not (isinstance(m1, int) and isinstance(m2, int) and m1 > 0 and m2 > 0):
            neg_q = False
        else:
            # The intersection of m1*Z and m2*Z is lcm(m1, m2)*Z.
            # The product ideal is (m1*m2)*Z.
            # They are equal iff lcm(m1, m2) == m1*m2, which is equivalent to gcd(m1, m2) == 1.
            # The conclusion fails if they are not equal.
            neg_q = math.gcd(m1, m2) != 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m1 and m2 are positive integers",
    "H_2: I is the ideal m1*Z",
    "H_3: J is the ideal m2*Z",
    "¬Q: I ∩ J is not equal to I*J (i.e. gcd(m1, m2) != 1)"
]

N_HYP = 3
NEG_Q_INDEX = 3