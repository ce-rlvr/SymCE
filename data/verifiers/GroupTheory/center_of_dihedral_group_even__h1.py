import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a counterexample to the false conjecture.
    The witness should be a tuple (G, n) or (n, G) where G is a group and n is an integer.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            if isinstance(witness[0], (int, sympy.Integer)):
                n, G = witness[0], witness[1]
            elif isinstance(witness[1], (int, sympy.Integer)):
                G, n = witness[0], witness[1]
            else:
                G, n = witness[0], witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: n is an even integer greater than 2
    try:
        if isinstance(n, (int, sympy.Integer)):
            n_val = int(n)
            h1 = (n_val % 2 == 0) and (n_val > 2)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The center Z(G) does not have exactly 2 elements
    try:
        if hasattr(G, 'center'):
            c = G.center()
            if hasattr(c, 'order'):
                if callable(c.order):
                    order = c.order()
                else:
                    order = c.order
            else:
                order = len(list(c))
        else:
            # Fallback for groups without a center() method
            elements = list(G.elements)
            order = 0
            for g in elements:
                if all(g * h == h * g for h in elements):
                    order += 1
        neg_q = (order != 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an even integer greater than 2",
    "¬Q: The center Z(G) does not have exactly 2 elements"
]

N_HYP = 1
NEG_Q_INDEX = 1