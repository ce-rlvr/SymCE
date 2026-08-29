import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # Parse witness: can be a tuple (H, G) or just H (implying G = H)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            H, G = witness
        else:
            H = witness
            G = witness
        
        # H_1: H is a finite group (and G is a subgroup of H)
        h1 = isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup)
        if h1:
            h1 = all(g in H for g in G.generators)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            H, G = witness
        else:
            H = witness
            G = witness
            
        # ¬Q: The intersection of G and its centralizer C_H(G) in H is not the trivial subgroup.
        # Mathematically, for any subgroup G <= H, G \cap C_H(G) is exactly the center of G, Z(G).
        # Thus, the intersection is trivial if and only if Z(G) is trivial.
        center = G.center()
        order = center.order() if callable(center.order) else center.order
        neg_q = order > 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "¬Q: The intersection of G and its centralizer C_H(G) in H is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1