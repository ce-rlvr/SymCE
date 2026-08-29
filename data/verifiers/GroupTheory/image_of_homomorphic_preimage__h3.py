import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
        G = witness.get('G')
        H = witness.get('H')
        phi = witness.get('phi')
        B = witness.get('B')
    except Exception:
        return [False, False, False]
        
    def get_elements(obj):
        if hasattr(obj, 'elements'):
            return list(obj.elements)
        try:
            return list(obj)
        except TypeError:
            return [obj]
            
    def apply_phi(phi_obj, g):
        if isinstance(phi_obj, dict):
            return phi_obj[g]
        else:
            return phi_obj(g)

    # H_1: G and H are groups
    try:
        def is_group(grp):
            if hasattr(grp, 'is_group') and grp.is_group: 
                return True
            if isinstance(grp, PermutationGroup): 
                return True
            if isinstance(grp, list) and len(grp) > 0:
                try:
                    for a in grp:
                        for b in grp:
                            if a * b not in grp:
                                return False
                    return True
                except Exception:
                    return False
            return False
            
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False

    # H_2: \phi: G \to H is a group homomorphism
    try:
        G_els = get_elements(G)
        H_els = get_elements(H)
        
        is_func = True
        for g in G_els:
            try:
                val = apply_phi(phi, g)
                if val not in H_els:
                    is_func = False
                    break
            except Exception:
                is_func = False
                break
                
        is_hom = True
        if is_func:
            for g1 in G_els:
                for g2 in G_els:
                    if apply_phi(phi, g1 * g2) != apply_phi(phi, g1) * apply_phi(phi, g2):
                        is_hom = False
                        break
                if not is_hom:
                    break
        h2 = is_func and is_hom
    except Exception:
        h2 = False

    # ¬Q: The image \phi(\phi^{-1}(B)) is not equal to the intersection B \cap \phi(G)
    try:
        G_els = get_elements(G)
        B_list = get_elements(B) if B is not None else []
        
        # Compute \phi(G)
        phi_G = []
        for g in G_els:
            val = apply_phi(phi, g)
            if val not in phi_G:
                phi_G.append(val)
                
        # Compute B \cap \phi(G)
        intersection = []
        for b in B_list:
            if b in phi_G and b not in intersection:
                intersection.append(b)
                
        # Compute \phi^{-1}(B)
        preimage_B = []
        for g in G_els:
            val = apply_phi(phi, g)
            if val in B_list and g not in preimage_B:
                preimage_B.append(g)
                
        # Compute \phi(\phi^{-1}(B))
        image_preimage = []
        for g in preimage_B:
            val = apply_phi(phi, g)
            if val not in image_preimage:
                image_preimage.append(val)
                
        def is_subset(l1, l2):
            for x in l1:
                if x not in l2:
                    return False
            return True
            
        # Check if they are NOT equal as sets
        neg_q = not (is_subset(intersection, image_preimage) and is_subset(image_preimage, intersection))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: \phi: G \to H is a group homomorphism",
    "¬Q: The image \phi(\phi^{-1}(B)) is not equal to the intersection B \cap \phi(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2