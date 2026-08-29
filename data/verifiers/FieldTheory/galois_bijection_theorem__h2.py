import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    """
    witness is expected to be a tuple (Gal_K_F, G) or a dict with these keys.
    Gal_K_F represents the Galois group of the finite Galois extension K/F.
    G represents the group G.
    """
    try:
        if isinstance(witness, dict):
            Gal_K_F = witness.get('Gal_K_F')
            G = witness.get('G')
        else:
            Gal_K_F, G = witness
    except Exception:
        return [False, False, False, False]

    # H1: K is a finite Galois extension of a field F
    # We verify this by checking that its Galois group is a valid finite permutation group.
    try:
        h1 = isinstance(Gal_K_F, PermutationGroup)
    except Exception:
        h1 = False

    # H2: \mathcal{I} is the set of all intermediate fields between F and K
    # This is a definitional setup step that is always true in context.
    h2 = True

    # H3: \mathcal{S} is the set of all subgroups of G
    # We verify this by checking that G is a valid finite permutation group.
    try:
        h3 = isinstance(G, PermutationGroup)
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails
    # The conclusion states that the map E -> Gal(K/E) is a bijection to the subgroups of G.
    # Since the image of this map is exactly the set of subgroups of Gal(K/F),
    # the map is a well-defined bijection to \mathcal{S} if and only if Gal(K/F) == G.
    # Therefore, the conclusion fails (neg_Q is True) iff Gal(K/F) != G.
    try:
        neg_q = (Gal_K_F != G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a finite Galois extension of a field F",
    "H_2: \mathcal{I} is the set of all intermediate fields between F and K",
    "H_3: \mathcal{S} is the set of all subgroups of G",
    "¬Q: The map E -> Gal(K/E) is not a bijection to the subgroups of G"
]

N_HYP = 3
NEG_Q_INDEX = 3