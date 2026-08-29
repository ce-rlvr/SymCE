import sympy
from sympy.ntheory import primefactors

# Top-level setup for rings
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12
ZZ = 0
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        # The witness could be a ring R, or a tuple (R, m)
        if isinstance(witness, tuple) and len(witness) > 0:
            ring = witness[0]
        else:
            ring = witness

        # Determine the number of closed points (maximal ideals) in Spec(R)
        if ring == sympy.ZZ:
            num_closed_points = float('inf')
        elif ring == sympy.QQ:
            num_closed_points = 1
        elif isinstance(ring, (int, sympy.Integer)):
            n = abs(int(ring))
            if n == 0:
                num_closed_points = float('inf')
            elif n == 1:
                num_closed_points = 0
            else:
                num_closed_points = len(primefactors(n))
        else:
            return [False]
            
        # The conclusion states that Spec(R) contains EXACTLY ONE closed point.
        # The negated conclusion is True if it does NOT contain exactly one closed point.
        neg_q = (num_closed_points != 1)
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: Spec(R) does not contain exactly one closed point"
]

N_HYP = 0
NEG_Q_INDEX = 0