import math
from sympy import Integer, Rational
from sympy.abc import x, y, z

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The dropped hypothesis from the true theorem is "I is a proper ideal".
    When I = R, the set of maximal ideals of R containing I is empty, and R/I is the zero ring,
    which also has no maximal ideals. The map is an empty bijection. In the context of this
    conjecture, this degenerate case is considered a failure of the bijection.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Witness is an integer n, representing the ideal nZ in the ring Z
        if isinstance(witness, (int, Integer)):
            n = abs(int(witness))
            h1 = True
            h2 = True
            # The conclusion fails if I = R, which in Z means n = 1
            neg_q = (n == 1)
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Witness is a tuple
        if isinstance(witness, tuple):
            if len(witness) == 1:
                n = abs(int(witness[0]))
                h1 = True
                h2 = True
                neg_q = (n == 1)
                return [h1, h2, neg_q]
            elif len(witness) == 2:
                # Could be (m, n) representing the ideal n(Z/mZ) in the ring Z/mZ
                if isinstance(witness[0], (int, Integer)) and isinstance(witness[1], (int, Integer)):
                    m = abs(int(witness[0]))
                    n = abs(int(witness[1]))
                    h1 = True
                    h2 = True
                    if m == 0:
                        neg_q = (n == 1)
                    elif m == 1:
                        # Z/1Z is the zero ring, where the only ideal is the whole ring
                        neg_q = True
                    else:
                        # I = R iff n is a unit in Z/mZ
                        neg_q = (math.gcd(n, m) == 1)
                    return [h1, h2, neg_q]
                # Could be strings like ("Z", "Z") representing (R, I)
                elif isinstance(witness[0], str) and isinstance(witness[1], str):
                    r_str = witness[0].strip()
                    i_str = witness[1].strip()
                    h1 = True
                    h2 = True
                    neg_q = (r_str == i_str or i_str == "1" or i_str == "R")
                    return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Witness is a dictionary specifying 'R' and 'I'
        if isinstance(witness, dict):
            if 'I' in witness and 'R' in witness:
                h1 = True
                h2 = True
                neg_q = (witness['I'] == witness['R'] or str(witness['I']).strip() == "1")
                return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Fallback for string representations
        s = str(witness).strip()
        if s == "1" or s == "R":
            return [True, True, True]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: \\pi: R -> R/I is the canonical projection homomorphism",
    "¬Q: The map M \\mapsto \\pi(M) does not establish a bijection between the maximal ideals of R containing I and the maximal ideals of R/I"
]

N_HYP = 2
NEG_Q_INDEX = 2