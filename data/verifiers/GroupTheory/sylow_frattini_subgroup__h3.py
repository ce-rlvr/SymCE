import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, P) or (G, Phi_G, P) where G is a finite group
    and P is a subgroup of G.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, P = witness
            elif len(witness) == 3:
                G, Phi_G, P = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: Let G be a finite group.
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: Let \Phi(G) be the Frattini subgroup of G.
    # This is a definitional hypothesis. We verify that P is a valid subgroup of G
    # so that the conclusion "P is a normal subgroup of G" is well-posed.
    try:
        h2 = isinstance(P, PermutationGroup) and P.is_subgroup(G)
    except Exception:
        h2 = False

    # neg_Q: P is NOT a normal subgroup of G.
    try:
        neg_q = not P.is_normal(G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: \\Phi(G) is the Frattini subgroup of G",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2