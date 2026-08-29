import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, X, x = witness
        elif len(witness) == 2:
            G, x = witness
            X = set(range(G.degree)) if hasattr(G, 'degree') else set()
        else:
            G, X, x = None, None, None
    except Exception:
        G, X, x = None, None, None

    # H1: G is an abelian group
    try:
        h1 = getattr(G, 'is_abelian', False)
        if callable(h1):
            h1 = h1()
        h1 = bool(h1)
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, frozenset, list, tuple))
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # neg_Q: The point stabilizer G_x is not equal to the kernel of the action.
    # The kernel is the set of elements in G that fix all y in X.
    # G_x is the set of elements in G that fix x.
    # Since kernel is always a subset of G_x, G_x != kernel iff there is some g in G_x not in the kernel.
    try:
        neg_q = False
        if G is not None and X is not None and x is not None:
            for g in G.elements:
                if g(x) == x:
                    fixes_all = True
                    for y in X:
                        if g(y) != y:
                            fixes_all = False
                            break
                    if not fixes_all:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: X is a set",
    "H_3: x is an element of X",
    "¬Q: The point stabilizer G_x is not equal to the kernel of the action"
]

N_HYP = 3
NEG_Q_INDEX = 3