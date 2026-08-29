import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: C_n is a cyclic group of order n",
    "¬Q: G is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n, C_n, G = None, None, None
    try:
        if isinstance(witness, dict):
            n = witness.get('n', 1)
            C_n = witness.get('C_n', CyclicGroup(n) if isinstance(n, int) and n > 0 else None)
            G = witness.get('G')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                n, C_n, G = witness
            elif len(witness) == 2:
                n, G = witness
                if isinstance(n, int) and n > 0:
                    C_n = CyclicGroup(n)
            elif len(witness) == 1:
                G = witness[0]
                n = 1
                C_n = CyclicGroup(1)
        else:
            G = witness
            n = 1
            C_n = CyclicGroup(1)
    except Exception:
        pass

    # H1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H2: C_n is a cyclic group of order n
    try:
        h2 = False
        if h1 and C_n is not None:
            if hasattr(C_n, 'order') and C_n.order() == n:
                if hasattr(C_n, 'generators') and any(g.order() == n for g in C_n.generators):
                    h2 = True
                elif n == 1 and C_n.order() == 1:
                    h2 = True
                elif hasattr(C_n, 'elements') and n <= 1000:
                    if any(g.order() == n for g in C_n.elements):
                        h2 = True
    except Exception:
        h2 = False

    # neg_Q: G is not solvable
    try:
        neg_q = False
        if G is not None and hasattr(G, 'is_solvable'):
            if G.is_solvable is False:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]