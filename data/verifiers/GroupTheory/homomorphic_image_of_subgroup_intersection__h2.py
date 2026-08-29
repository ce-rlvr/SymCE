import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy import eye, zeros
import math
import itertools
import functools

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
    Checks if the witness is a valid counterexample to the false conjecture:
    "The image phi(A \cap B) is a subset of phi(A) \cap phi(B)."
    
    (Note: phi(A \cap B) is ALWAYS a subset of phi(A) \cap phi(B). The dropped hypothesis 
    from the true theorem is that phi is injective, which guarantees equality. 
    The intended false conclusion is that they are equal or that the reverse inclusion holds.
    We check if they are NOT equal to correctly identify the counterexample.)
    """
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        A = witness.get('A')
        B = witness.get('B')
        phi = witness.get('phi')
    else:
        try:
            G, H, A, B, phi = witness
        except Exception:
            return [False, False, False, False]

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: A and B are subgroups of G
    try:
        h2 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup) and A.is_subgroup(G) and B.is_subgroup(G)
    except Exception:
        h2 = False

    # H3: phi is a homomorphism from G to H
    try:
        if not h1:
            h3 = False
        else:
            G_elements = list(G.generate())
            h3 = True
            
            if callable(phi):
                phi_dict = {g: phi(g) for g in G_elements}
            elif isinstance(phi, dict):
                phi_dict = phi
            elif isinstance(phi, (list, tuple)):
                phi_dict = dict(phi)
            else:
                h3 = False
                phi_dict = {}
            
            if h3:
                for g in G_elements:
                    if g not in phi_dict:
                        h3 = False
                        break
                    if not H.contains(phi_dict[g]):
                        h3 = False
                        break
            if h3:
                for g1 in G_elements:
                    for g2 in G_elements:
                        if phi_dict[g1 * g2] != phi_dict[g1] * phi_dict[g2]:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails (phi(A \cap B) != phi(A) \cap phi(B))
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            A_elements = list(A.generate())
            B_elements = list(B.generate())
            A_cap_B = [g for g in A_elements if B.contains(g)]
            
            phi_A = set(phi_dict[g] for g in A_elements)
            phi_B = set(phi_dict[g] for g in B_elements)
            phi_A_cap_B = set(phi_dict[g] for g in A_cap_B)
            
            intersection_of_images = phi_A.intersection(phi_B)
            
            # The conclusion fails if the image of the intersection does not equal the intersection of the images
            neg_q = (phi_A_cap_B != intersection_of_images)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A and B are subgroups of G",
    "H_3: phi is a homomorphism from G to H",
    "¬Q: The image phi(A \\cap B) does not equal phi(A) \\cap phi(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3