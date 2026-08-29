import sympy
from sympy import GF, QQ, RR, CC

# Top-level setup: named object bindings for witness expressions
F2 = GF(2)
F3 = GF(3)
F5 = GF(5)
F7 = GF(7)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    'For any field K, GL_n(K) equipped with the Zariski topology is a connected topological space.'
    
    A valid witness is a tuple (K, n) where K is a finite field and n is an integer >= 1
    such that |GL_n(K)| > 1 (which makes it a discrete space with >1 points, hence disconnected).
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        K, n = witness
        # H_1: K is a field and n is a positive integer
        h1 = getattr(K, 'is_Field', False) and isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # ¬Q: GL_n(K) is NOT connected in the Zariski topology.
            # In the Zariski topology, GL_n(K) is connected for any infinite field K.
            # For a finite field K, the Zariski topology is discrete, so it is connected
            # if and only if it has exactly 1 element.
            if hasattr(K, 'order') and K.order != sympy.oo:
                q = int(K.order)
                order_gl = 1
                for i in range(n):
                    order_gl *= (q**n - q**i)
                neg_q = order_gl > 1
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field and n is a positive integer",
    "¬Q: GL_n(K) is not connected in the Zariski topology"
]

N_HYP = 1
NEG_Q_INDEX = 1