import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    try:
        # H1: G is a finite group
        # In SymPy, PermutationGroup instances represent finite groups.
        h1 = isinstance(witness, sympy.combinatorics.PermutationGroup)
    except Exception:
        h1 = False

    try:
        # H2: G is an abelian group
        h2 = bool(witness.is_abelian)
    except Exception:
        h2 = False

    try:
        # ¬Q: G is NOT isomorphic to the group of all group homomorphisms from G to C*
        # For any finite group G, the character group Hom(G, C*) is isomorphic to its 
        # abelianization G/[G,G]. Therefore, |Hom(G, C*)| = |G/[G,G]|.
        # G is isomorphic to Hom(G, C*) if and only if |G| == |G/[G,G]|, which occurs 
        # if and only if [G,G] is trivial (i.e., G is abelian).
        # Thus, for finite groups, G is NOT isomorphic to Hom(G, C*) iff G is NOT abelian.
        if isinstance(witness, sympy.combinatorics.PermutationGroup):
            neg_q = not witness.is_abelian
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is an abelian group",
    "¬Q: G is not isomorphic to the group of all group homomorphisms from G to C*"
]

N_HYP = 2
NEG_Q_INDEX = 2