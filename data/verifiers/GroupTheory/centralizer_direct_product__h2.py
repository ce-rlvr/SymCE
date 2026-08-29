import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H, g, h = witness
    except Exception:
        return [False, False, False]
        
    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: h is an element of H
    try:
        h2 = h in H
    except Exception:
        h2 = False
        
    # Conclusion: The centralizer of the element (g, h) in the direct product G × H is equal to C_G(g) × C_H(h).
    try:
        # The centralizer of an element in a group is only well-defined if the element belongs to the group.
        # If g is not in G, then (g, h) is not in G x H, making the centralizer undefined (equality fails).
        if g not in G:
            q = False
        elif h not in H:
            q = False
        else:
            # If both elements are in their respective groups, we compute the centralizers.
            C_G_g = {x for x in G.elements if x * g == g * x}
            C_H_h = {y for y in H.elements if y * h == h * y}
            
            # Compute C_{G x H}(g, h)
            C_GxH = set()
            for x in G.elements:
                for y in H.elements:
                    if (x * g == g * x) and (y * h == h * y):
                        C_GxH.add((x, y))
                        
            # Cartesian product C_G(g) x C_H(h)
            rhs = {(x, y) for x in C_G_g for y in C_H_h}
            
            q = (C_GxH == rhs)
    except Exception:
        q = False
        
    neg_q = not q
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: h is an element of H",
    "¬Q: The centralizer of (g, h) in G x H is not equal to C_G(g) x C_H(h)"
]

N_HYP = 2
NEG_Q_INDEX = 2