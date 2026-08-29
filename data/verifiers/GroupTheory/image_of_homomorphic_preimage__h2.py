import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False]
        G, H, B, phi = witness
    except Exception:
        return [False, False, False]
    
    # H1: G and H are groups
    try:
        def is_grp(X):
            if isinstance(X, PermutationGroup):
                return True
            if hasattr(X, 'elements') and hasattr(X, 'identity'):
                return True
            return False
        h1 = is_grp(G) and is_grp(H)
    except Exception:
        h1 = False

    # H2: B is a subgroup of H
    try:
        if hasattr(B, 'is_subgroup'):
            h2 = bool(B.is_subgroup(H))
        else:
            B_elems = set(B.elements)
            H_elems = set(H.elements)
            h2 = is_grp(B) and B_elems.issubset(H_elems)
    except Exception:
        h2 = False

    # neg_Q: The image \phi(\phi^{-1}(B)) is equal to the intersection B \cap \phi(G).
    # We return True if they are NOT equal (i.e., the conclusion fails).
    # Note: For any single-valued function, this set-theoretic identity is always true.
    # The conjecture fails when \phi is a relation (multi-valued function).
    try:
        G_elems = set(G.elements)
        B_elems = set(B.elements)
        
        def get_rel_image(phi_obj, X):
            if isinstance(phi_obj, dict):
                res = set()
                for x in X:
                    if x in phi_obj:
                        val = phi_obj[x]
                        if isinstance(val, (set, list, tuple)):
                            res.update(val)
                        else:
                            res.add(val)
                return res
            elif isinstance(phi_obj, (set, list, tuple)):
                return {y for x, y in phi_obj if x in X}
            elif callable(phi_obj):
                res = set()
                for x in X:
                    try:
                        val = phi_obj(x)
                        if isinstance(val, (set, list, tuple)):
                            res.update(val)
                        else:
                            res.add(val)
                    except Exception:
                        pass
                return res
            return set()

        def get_rel_preimage(phi_obj, Y, domain):
            if isinstance(phi_obj, dict):
                res = set()
                for x in domain:
                    if x in phi_obj:
                        val = phi_obj[x]
                        if isinstance(val, (set, list, tuple)):
                            if any(v in Y for v in val):
                                res.add(x)
                        else:
                            if val in Y:
                                res.add(x)
                return res
            elif isinstance(phi_obj, (set, list, tuple)):
                return {x for x, y in phi_obj if x in domain and y in Y}
            elif callable(phi_obj):
                res = set()
                for x in domain:
                    try:
                        val = phi_obj(x)
                        if isinstance(val, (set, list, tuple)):
                            if any(v in Y for v in val):
                                res.add(x)
                        else:
                            if val in Y:
                                res.add(x)
                    except Exception:
                        pass
                return res
            return set()

        phi_inv_B = get_rel_preimage(phi, B_elems, G_elems)
        image_phi_inv_B = get_rel_image(phi, phi_inv_B)
        
        phi_G = get_rel_image(phi, G_elems)
        B_cap_phi_G = B_elems.intersection(phi_G)
        
        neg_q = (image_phi_inv_B != B_cap_phi_G)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: B is a subgroup of H",
    "¬Q: The image phi(phi^-1(B)) is not equal to B \\cap phi(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2