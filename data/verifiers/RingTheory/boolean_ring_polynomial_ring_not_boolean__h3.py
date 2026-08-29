import sympy
from sympy import polys

# Top-level setup
try:
    GF2 = polys.domains.GF(2)
except Exception:
    GF2 = None

def conditions(witness):
    # H_1: R is a Boolean ring
    h1 = False
    try:
        if isinstance(witness, int):
            h1 = (witness == 1 or witness == 2)
        elif GF2 is not None and witness == GF2:
            h1 = True
        elif hasattr(witness, 'is_Boolean_ring'):
            h1 = bool(witness.is_Boolean_ring())
        elif hasattr(witness, 'elements') and hasattr(witness, 'mul'):
            h1 = True
            for x in witness.elements:
                if witness.mul(x, x) != x:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: R has at least two elements
    h2 = False
    try:
        if isinstance(witness, int):
            h2 = (witness >= 2)
        elif GF2 is not None and witness == GF2:
            h2 = True
        elif hasattr(witness, 'order'):
            if callable(witness.order):
                h2 = int(witness.order()) >= 2
            else:
                h2 = int(witness.order) >= 2
        elif hasattr(witness, 'elements'):
            if hasattr(witness.elements, '__len__'):
                h2 = len(witness.elements) >= 2
            else:
                count = 0
                for _ in witness.elements:
                    count += 1
                    if count >= 2:
                        break
                h2 = count >= 2
    except Exception:
        h2 = False

    # ¬Q: R[x] is a Boolean ring
    # In any polynomial ring R[x], the element x satisfies x^2 = x only if 1 = 0 in R.
    # Thus, R[x] is a Boolean ring if and only if R is the trivial ring (1 element).
    neg_q = False
    try:
        if isinstance(witness, int):
            neg_q = (witness == 1)
        elif GF2 is not None and witness == GF2:
            neg_q = False
        elif hasattr(witness, 'order'):
            if callable(witness.order):
                neg_q = int(witness.order()) == 1
            else:
                neg_q = int(witness.order) == 1
        elif hasattr(witness, 'elements'):
            if hasattr(witness.elements, '__len__'):
                neg_q = len(witness.elements) == 1
            else:
                count = 0
                for _ in witness.elements:
                    count += 1
                    if count > 1:
                        break
                neg_q = count == 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R has at least two elements",
    "not Q: Polynomial ring over R is a Boolean ring"
]

N_HYP = 2
NEG_Q_INDEX = 2