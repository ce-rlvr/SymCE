import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(0))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: phi is a surjective group homomorphism from G to H
    try:
        if not h1:
            h2 = False
        else:
            G_elements = list(G.generate())
            H_elements = list(H.generate())
            
            if callable(phi):
                mapping = {g: phi(g) for g in G_elements}
            elif isinstance(phi, dict):
                mapping = phi
            else:
                mapping = {}
                
            if not all(g in mapping for g in G_elements):
                h2 = False
            elif not all(mapping[g] in H_elements for g in G_elements):
                h2 = False
            else:
                is_homo = True
                for g1 in G_elements:
                    for g2 in G_elements:
                        if mapping[g1 * g2] != mapping[g1] * mapping[g2]:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                
                if not is_homo:
                    h2 = False
                else:
                    image = set(mapping[g] for g in G_elements)
                    h2 = (image == set(H_elements))
    except Exception:
        h2 = False
        
    # neg_Q: H is not a cyclic group
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            H_elements = list(H.generate())
            H_order = H.order() if callable(H.order) else H.order
            
            is_cyclic = False
            for h in H_elements:
                h_order = h.order() if callable(h.order) else h.order
                if h_order == H_order:
                    is_cyclic = True
                    break
            neg_q = not is_cyclic
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a surjective group homomorphism from G to H",
    "¬Q: H is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2