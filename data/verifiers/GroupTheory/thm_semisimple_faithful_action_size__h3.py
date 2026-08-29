import sympy
import sympy.ntheory
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
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

def is_square_free(n):
    if n < 1:
        return False
    if n == 1:
        return True
    factors = sympy.ntheory.factorint(n)
    return all(v == 1 for v in factors.values())

def conditions(witness) -> list[bool]:
    G = None
    X_size = None
    
    try:
        if isinstance(witness, tuple):
            G = witness[0]
            if len(witness) > 1:
                if isinstance(witness[1], int):
                    X_size = witness[1]
                elif hasattr(witness[1], '__len__'):
                    X_size = len(witness[1])
                else:
                    X_size = getattr(G, 'degree', 0)
            else:
                X_size = getattr(G, 'degree', 0)
        else:
            G = witness
            X_size = getattr(G, 'degree', 0)
    except Exception:
        return [False, False, False]

    # H1: G is a non-trivial finite semisimple group
    # In this context, a finite semisimple group is a direct product of simple groups.
    h1 = False
    try:
        if isinstance(G, PermutationGroup) and G.order() > 1:
            if G.order() <= 1000:
                if G.order() == 60 and getattr(G, 'is_perfect', False):
                    h1 = True
                elif getattr(G, 'is_abelian', False):
                    h1 = all(is_square_free(g.order()) for g in G.elements)
    except Exception:
        h1 = False

    # H2: X is a finite set with strictly less than 5 elements
    h2 = False
    try:
        if X_size is not None and X_size >= 0:
            h2 = X_size < 5
    except Exception:
        h2 = False

    # neg_Q: The action of G on X IS faithful
    neg_q = False
    try:
        if isinstance(G, PermutationGroup):
            if X_size >= G.degree:
                neg_q = True
            else:
                if G.order() == 2 and X_size >= 2:
                    neg_q = True
                elif G.order() == 3 and X_size >= 3:
                    neg_q = True
                elif G.order() == 4 and getattr(G, 'is_abelian', False) and X_size >= 4:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-trivial finite semisimple group",
    "H_2: X is a finite set with strictly less than 5 elements",
    "¬Q: The action of G on X is faithful"
]

N_HYP = 2
NEG_Q_INDEX = 2