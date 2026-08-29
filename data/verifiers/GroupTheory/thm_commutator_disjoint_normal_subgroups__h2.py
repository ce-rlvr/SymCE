import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(H, PermutationGroup) and 
              isinstance(K, PermutationGroup) and 
              all(G.contains(h) for h in H.generators) and 
              all(G.contains(k) for k in K.generators))
    except Exception:
        h1 = False

    try:
        h_elements = set(H.generate())
        k_elements = set(K.generate())
        h2 = len(h_elements.intersection(k_elements)) == 1
    except Exception:
        h2 = False

    try:
        neg_q = any(h * k != k * h for h in H.generators for k in K.generators)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and H and K are subgroups",
    "H_2: H and K have trivial intersection",
    "¬Q: The mutual commutator of H and K is not trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2