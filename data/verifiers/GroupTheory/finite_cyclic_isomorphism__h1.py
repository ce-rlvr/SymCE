import sympy
from sympy.combinatorics import PermutationGroup, Permutation, Cycle
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = None
            if hasattr(G, 'order'):
                n = G.order() if callable(G.order) else G.order
            elif type(G).__name__ == 'Cycle':
                n = len(G)
            else:
                try:
                    n = len(G)
                except Exception:
                    pass
    except Exception:
        return [False, False, False]

    # H1: G is cyclic
    h1 = False
    try:
        if hasattr(G, 'is_cyclic'):
            h1 = bool(G.is_cyclic)
        elif hasattr(G, 'cyclic_form'):
            cycles = [c for c in G.cyclic_form if len(c) > 1]
            h1 = (len(cycles) <= 1)
        elif type(G).__name__ == 'Cycle':
            h1 = True
    except Exception:
        pass

    # H2: The order of G is a finite integer n
    h2 = False
    try:
        if n is not None and isinstance(n, (int, sympy.Integer)):
            if hasattr(G, 'order'):
                order = G.order() if callable(G.order) else G.order
                h2 = (order == n)
            elif type(G).__name__ == 'Cycle':
                h2 = (len(G) == n)
            else:
                try:
                    h2 = (len(G) == n)
                except Exception:
                    pass
    except Exception:
        pass

    # neg_Q: G is not isomorphic to Z_n
    neg_q = False
    try:
        is_group = isinstance(G, PermutationGroup)
        if is_group:
            if getattr(G, 'is_cyclic', False) and getattr(G, 'order', lambda: None)() == n:
                neg_q = False
            else:
                neg_q = True
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is cyclic",
    "H_2: The order of G is a finite integer n",
    "¬Q: G is not isomorphic to the additive group Z_n of integers modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2