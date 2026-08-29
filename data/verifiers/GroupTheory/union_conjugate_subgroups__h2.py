import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(H, PermutationGroup) and 
              all(gen in G for gen in H.generators))
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            union_elements = set()
            G_elements = list(G.generate())
            H_elements = list(H.generate())
            for g in G_elements:
                g_inv = g**-1
                for h in H_elements:
                    union_elements.add(g * h * g_inv)
            neg_q = len(union_elements) == len(G_elements)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group and H is a subgroup of G",
    "¬Q: The union of all conjugate subgroups gHg^{-1} is not a proper subset of G"
]

N_HYP = 1
NEG_Q_INDEX = 1