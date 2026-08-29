import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Unpack witness. It can be a tuple (G, x) or just G (defaulting x to 0).
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x = witness
        else:
            G = witness
            x = 0
    except Exception:
        return [False, False, False, False]

    # H_1: X is a set
    # In SymPy, a PermutationGroup implicitly defines a set (its domain).
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G acts transitively on X
    try:
        if callable(G.is_transitive):
            h2 = bool(G.is_transitive())
        else:
            h2 = bool(G.is_transitive)
    except Exception:
        h2 = False

    # H_3: x is an element of X
    try:
        if callable(G.degree):
            degree = G.degree()
        else:
            degree = G.degree
        h3 = isinstance(x, int) and 0 <= x < degree
    except Exception:
        h3 = False

    # ¬Q: The point stabilizer G_x is NOT equal to the kernel of the action of G on X.
    # For a PermutationGroup acting naturally on its domain, the action is faithful,
    # meaning the kernel of the action is always the trivial group (order 1).
    # Therefore, G_x == Kernel if and only if the stabilizer G_x has order 1.
    # The negated conclusion (conclusion fails) means G_x has order > 1.
    try:
        stab = G.stabilizer(x)
        if callable(stab.order):
            order = stab.order()
        else:
            order = stab.order
        neg_q = order != 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts transitively on X",
    "H_3: x is an element of X",
    "¬Q: The point stabilizer G_x is not equal to the kernel of the action"
]

N_HYP = 3
NEG_Q_INDEX = 3