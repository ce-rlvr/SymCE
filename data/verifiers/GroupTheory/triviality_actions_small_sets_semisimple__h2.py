import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
    G = None
    X_size = None
    
    try:
        if isinstance(witness, PermutationGroup):
            G = witness
            X_size = G.degree
        elif isinstance(witness, list) and len(witness) > 0 and all(isinstance(p, Permutation) for p in witness):
            G = PermutationGroup(witness)
            X_size = G.degree
        elif isinstance(witness, tuple):
            if len(witness) >= 1:
                if isinstance(witness[0], PermutationGroup):
                    G = witness[0]
                    X_size = G.degree
                elif isinstance(witness[0], list) and len(witness[0]) > 0 and all(isinstance(p, Permutation) for p in witness[0]):
                    G = PermutationGroup(witness[0])
                    X_size = G.degree
            if len(witness) >= 2:
                try:
                    X_size = len(witness[1])
                except Exception:
                    pass
    except Exception:
        pass

    try:
        # H_1: G is a finite group
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        # H_2: X is a set
        # A PermutationGroup naturally acts on a finite set (its domain)
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    try:
        # H_3: The cardinality of X is less than or equal to 4
        h3 = False
        if h2 and X_size is not None:
            h3 = bool(X_size <= 4)
    except Exception:
        h3 = False

    try:
        # H_4: G acts on the set X
        h4 = isinstance(G, PermutationGroup)
    except Exception:
        h4 = False

    try:
        # ¬Q: The action of G on X is not the trivial action
        # The action is trivial iff the group only contains the identity permutation.
        neg_q = False
        if isinstance(G, PermutationGroup):
            neg_q = bool(G.order() > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a set",
    "H_3: The cardinality of X is less than or equal to 4",
    "H_4: G acts on the set X",
    "¬Q: The action of G on X is not the trivial action"
]

N_HYP = 4
NEG_Q_INDEX = 4