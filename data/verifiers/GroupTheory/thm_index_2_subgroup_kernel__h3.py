import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2_ok = False
        
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
            neg_q_ok = False
        else:
            # The conclusion states there exists a surjective homomorphism from G to Z_2 with kernel H.
            # By the First Isomorphism Theorem, this is equivalent to H being a normal subgroup of G
            # and the quotient group G/H being isomorphic to Z_2 (which means [G:H] = 2).
            is_normal = H.is_normal(G)
            index_is_2 = (G.order() == 2 * H.order())
            conclusion_holds = is_normal and index_is_2
            neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: There does not exist a surjective group homomorphism from G to Z_2 with kernel H"
]

N_HYP = 2
NEG_Q_INDEX = 2