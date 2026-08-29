import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Standard group theory objects
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

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    Expected witness format: (G, H, mapping)
    where mapping is a dictionary or callable mapping elements of G to elements of H.
    """
    try:
        G, H, mapping = witness[:3]
    except Exception:
        return [False, False, False]

    # H_1: f: G \to H is a surjective group homomorphism
    try:
        if callable(mapping):
            map_func = mapping
        else:
            map_func = lambda g: mapping[g]
            
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        
        mapped_elements = []
        for g in G_elements:
            mapped_elements.append(map_func(g))
            
        if not all(m in H_elements for m in mapped_elements):
            h1 = False
        else:
            is_homo = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if map_func(g1 * g2) != map_func(g1) * map_func(g2):
                        is_homo = False
                        break
                if not is_homo:
                    break
            
            image = set(mapped_elements)
            is_surj = (image == set(H_elements))
            
            h1 = is_homo and is_surj
    except Exception:
        h1 = False

    # H_2: Z(G) is the center of G
    # This is a definitional hypothesis. We verify that G has a computable center.
    try:
        if hasattr(G, 'center'):
            Z_G = G.center()
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The image f(Z(G)) is NOT a subgroup of the center of H
    try:
        if callable(mapping):
            map_func = mapping
        else:
            map_func = lambda g: mapping[g]

        Z_G = G.center()
        Z_H = H.center()
        
        image_Z_G = set(map_func(z) for z in Z_G.elements)
        Z_H_elements = set(Z_H.elements)
        
        is_subset = image_Z_G.issubset(Z_H_elements)
        
        is_subgroup = is_subset
        if is_subgroup:
            # Check closure under multiplication
            for x in image_Z_G:
                for y in image_Z_G:
                    if x * y not in image_Z_G:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            # Check closure under inverses
            if is_subgroup:
                for x in image_Z_G:
                    if x**-1 not in image_Z_G:
                        is_subgroup = False
                        break
                    
        neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f: G \\to H is a surjective group homomorphism",
    "H_2: Z(G) is the center of G",
    "¬Q: The image f(Z(G)) is not a subgroup of the center of H"
]

N_HYP = 2
NEG_Q_INDEX = 2