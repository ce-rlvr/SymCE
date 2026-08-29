import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.homomorphisms import homomorphism

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If G and H are groups, phi is a homomorphism from G to H, and A, B are subgroups of G,
    then phi(A) and phi(B) are conjugate in H."
    """
    try:
        if len(witness) != 5:
            return [False, False, False, False]
        G, H, phi, A, B = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    h2 = False
    mapping = None
    try:
        if h1:
            G_elems = list(G.elements)
            if isinstance(phi, dict):
                if all(g in phi for g in G_elems):
                    mapping = phi
                else:
                    hom = homomorphism(G, H, G.generators, [phi[g] for g in G.generators])
                    mapping = {g: hom(g) for g in G_elems}
            elif callable(phi):
                mapping = {g: phi(g) for g in G_elems}
            
            if mapping is not None:
                H_elems = set(H.elements)
                h2 = True
                # Check if all images are in H
                for v in mapping.values():
                    if v not in H_elems:
                        h2 = False
                        break
                # Check homomorphism property: phi(x*y) == phi(x)*phi(y)
                if h2:
                    for x in G_elems:
                        for y in G_elems:
                            if mapping[x * y] != mapping[x] * mapping[y]:
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # H_3: A and B are subgroups of G
    try:
        h3 = False
        if isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup):
            G_elems_set = set(G.elements)
            
            A_is_sub = False
            try:
                A_is_sub = A.is_subgroup(G)
            except Exception:
                pass
            if not A_is_sub:
                A_is_sub = set(A.elements).issubset(G_elems_set)
                
            B_is_sub = False
            try:
                B_is_sub = B.is_subgroup(G)
            except Exception:
                pass
            if not B_is_sub:
                B_is_sub = set(B.elements).issubset(G_elems_set)
                
            h3 = A_is_sub and B_is_sub
    except Exception:
        h3 = False

    # ¬Q: phi(A) and phi(B) are NOT conjugate in H
    neg_q = False
    try:
        if h1 and h3 and mapping is not None:
            img_A_elems = set(mapping[a] for a in A.elements)
            img_B_elems = set(mapping[b] for b in B.elements)
            
            are_conjugate = False
            for h in H.elements:
                h_inv = ~h
                conj_A_elems = set((h * a * h_inv) for a in img_A_elems)
                if conj_A_elems == img_B_elems:
                    are_conjugate = True
                    break
            neg_q = not are_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "H_3: A and B are subgroups of G",
    "¬Q: phi(A) and phi(B) are not conjugate in H"
]

N_HYP = 3
NEG_Q_INDEX = 3