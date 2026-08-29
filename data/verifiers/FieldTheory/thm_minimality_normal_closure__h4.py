import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Witness is expected to be a tuple of three PermutationGroups: (G, H_E, H_L)
# representing the Galois correspondence of the fields:
# G    <--> F
# H_E  <--> E
# H_L  <--> L
# {id} <--> K

CONDITION_LABELS = [
    "H_1: E/F is an algebraic field extension (G is a finite group, H_E <= G)",
    "H_2: K is the normal closure of E over F (core_G(H_E) == {id})",
    "H_3: L is an intermediate field such that E <= L <= K (H_L <= H_E)",
    "¬Q: L is not equal to K (H_L != {id})"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G, H_E, H_L = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: E/F is an algebraic field extension
    try:
        if not (isinstance(G, PermutationGroup) and 
                isinstance(H_E, PermutationGroup) and 
                isinstance(H_L, PermutationGroup)):
            h1 = False
            G_elements = set()
        else:
            G_elements = set(G.generate())
            h1 = all(g in G_elements for g in H_E.generators)
    except Exception:
        h1 = False
        G_elements = set()

    # H_2: K is the normal closure of E over F
    try:
        if not h1:
            h2 = False
        else:
            H_E_elements = set(H_E.generate())
            core_elements = set(H_E_elements)
            for g in G_elements:
                g_inv = ~g
                conj_set = {g * h * g_inv for h in H_E_elements}
                core_elements = core_elements.intersection(conj_set)
                if len(core_elements) == 1:
                    break
            h2 = (len(core_elements) == 1)
    except Exception:
        h2 = False

    # H_3: L is an intermediate field such that E <= L <= K
    try:
        if not h1:
            h3 = False
        else:
            H_E_elements = set(H_E.generate())
            h3 = all(g in H_E_elements for g in H_L.generators)
    except Exception:
        h3 = False

    # ¬Q: L must be equal to K (Negation: L != K)
    try:
        if not h1:
            neg_q = False
        else:
            H_L_elements = set(H_L.generate())
            neg_q = len(H_L_elements) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]