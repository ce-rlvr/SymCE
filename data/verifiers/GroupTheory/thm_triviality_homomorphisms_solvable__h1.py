import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.homomorphisms import homomorphism, GroupHomomorphism

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    phi = None
    G = None
    S = None
    
    try:
        if isinstance(witness, GroupHomomorphism):
            phi = witness
            G = phi.domain
            S = phi.codomain
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, S, images = witness
    except Exception:
        pass

    try:
        h1 = False
        if S is not None:
            h1 = bool(S.is_solvable)
    except Exception:
        h1 = False

    try:
        h2 = False
        if phi is None and G is not None and S is not None:
            phi = homomorphism(G, S, images)
        if phi is not None:
            h2 = isinstance(phi, GroupHomomorphism)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if phi is not None:
            img = phi.image()
            neg_q = not (img.order() == 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a solvable group",
    "H_2: phi is a group homomorphism",
    "¬Q: The image of phi is not the trivial subgroup of S"
]

N_HYP = 2
NEG_Q_INDEX = 2