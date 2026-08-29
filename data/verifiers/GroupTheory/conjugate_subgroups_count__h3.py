import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if isinstance(H, list):
            H = PermutationGroup(H)
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            G_elements = list(G.generate())
            H_elements = frozenset(H.generate())
            
            conjugates = set()
            normalizer_size = 0
            
            for g in G_elements:
                g_inv = ~g
                conj = frozenset(g * h * g_inv for h in H_elements)
                conjugates.add(conj)
                
                if conj == H_elements:
                    normalizer_size += 1
                    
            index = len(G_elements) // normalizer_size
            neg_q = bool(len(conjugates) != index)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "¬Q: The number of distinct conjugate subgroups is not equal to the index of the normalizer"
]

N_HYP = 2
NEG_Q_INDEX = 2