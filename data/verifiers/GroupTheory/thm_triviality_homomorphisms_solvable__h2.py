import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics import PermutationGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    G = None
    S = None
    phi = None
    images = None

    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, S, images = witness
        else:
            # Check if it's already a GroupHomomorphism by class name to avoid strict import dependency
            if type(witness).__name__ == 'GroupHomomorphism':
                phi = witness
                G = phi.domain
                S = phi.codomain
    except Exception:
        pass

    # H1: G is a semisimple finite group
    # A finite group is semisimple iff it has no non-trivial solvable normal subgroups
    try:
        if G is not None and hasattr(G, 'normal_subgroups'):
            h1 = True
            for N in G.normal_subgroups():
                if N.order() > 1 and N.is_solvable:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: phi is a group homomorphism
    try:
        if phi is not None:
            h2 = True
        elif G is not None and S is not None and images is not None:
            from sympy.combinatorics.homomorphisms import homomorphism
            if isinstance(images, dict):
                phi = homomorphism(G, S, images)
            else:
                phi = homomorphism(G, S, G.generators, images)
            if phi is not None:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The image of phi is NOT the trivial subgroup of S
    try:
        if h2 and phi is not None:
            img = phi.image()
            if img.order() > 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: phi: G -> S is a group homomorphism",
    "¬Q: The image of phi is not the trivial subgroup of S"
]

N_HYP = 2
NEG_Q_INDEX = 2