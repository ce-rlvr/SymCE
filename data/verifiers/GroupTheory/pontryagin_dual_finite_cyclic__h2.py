import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: \widehat{G} is the Pontryagin dual of G",
    "¬Q: \widehat{G} is not isomorphic to G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, G_hat = witness
        else:
            G = witness
            G_hat = None
    except Exception:
        G = witness
        G_hat = None

    # H1: G is a finite cyclic group
    try:
        if isinstance(G, PermutationGroup):
            h1 = bool(G.is_cyclic)
        else:
            h1 = bool(getattr(G, 'is_finite', False) and getattr(G, 'is_cyclic', False))
    except Exception:
        h1 = False

    # H2: \widehat{G} is the Pontryagin dual of G
    try:
        if G_hat is not None:
            # The Pontryagin dual of a finite group G is isomorphic to its abelianization.
            # Thus, G_hat must be abelian and have the same abelian invariants as G.
            h2 = bool(G_hat.is_abelian and sorted(G_hat.abelian_invariants()) == sorted(G.abelian_invariants()))
        else:
            # If G_hat is not explicitly provided, we assume the witness is just G,
            # and H2 is trivially satisfied by the definition of the dual.
            h2 = True
    except Exception:
        h2 = False

    # Q: \widehat{G} is isomorphic to G
    try:
        if G_hat is not None:
            q = bool(G_hat.is_isomorphic(G))
        else:
            # If G_hat is not provided, we evaluate whether the Pontryagin dual of G is isomorphic to G.
            # The Pontryagin dual of G is isomorphic to its abelianization.
            # The abelianization is isomorphic to G iff G is abelian.
            if not hasattr(G, 'is_abelian'):
                raise ValueError("Witness is not a valid group")
            q = bool(G.is_abelian)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]