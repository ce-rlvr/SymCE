import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    # H_1: G is an abelian group
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # ¬Q: Hom(Z, G) is not isomorphic to G
    try:
        # Mathematically, for any abelian group G, the group of homomorphisms 
        # Hom(Z, G) is naturally isomorphic to G via the evaluation map f -> f(1).
        # Therefore, if G is abelian, the conclusion "Hom(Z, G) is isomorphic to G" 
        # is ALWAYS TRUE, meaning its negation is FALSE.
        # If G is not abelian, Hom(Z, G) does not naturally form a group, 
        # so it cannot be isomorphic to G as a group.
        if h1:
            neg_q = False
        else:
            # Check if it's at least a group-like object to meaningfully fail the conclusion
            if hasattr(witness, 'is_abelian'):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: Hom(Z, G) is not isomorphic to G"
]

N_HYP = 1
NEG_Q_INDEX = 1