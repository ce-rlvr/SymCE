import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The dropped hypothesis from the true theorem is "G is a group".
    """
    try:
        G, H, phi, M = witness
    except Exception:
        return [False, False, False, False]
        
    def get_image(f, x):
        if callable(f):
            return f(x)
        return f[x]
        
    def get_elements(grp):
        if hasattr(grp, 'elements'):
            return list(grp.elements)
        return list(grp)

    # H_1: H is a group
    try:
        h1 = isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: phi is a group homomorphism from G to H
    try:
        if type(phi).__name__ == 'Homomorphism':
            h2 = (phi.domain == G and phi.codomain == H)
        else:
            G_elems = get_elements(G)
            h2 = True
            # Check operation preservation
            for g1 in G_elems:
                for g2 in G_elems:
                    if get_image(phi, g1 * g2) != get_image(phi, g1) * get_image(phi, g2):
                        h2 = False
                        break
                if not h2:
                    break
            # Check codomain mapping
            if h2:
                for g in G_elems:
                    if get_image(phi, g) not in H:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # H_3: M is a normal subgroup of H
    try:
        h3 = M.is_subgroup(H) and M.is_normal(H)
    except Exception:
        h3 = False
        
    # ¬Q: The preimage phi^{-1}(M) is NOT a normal subgroup of G
    try:
        G_elems = get_elements(G)
        preimage_elements = [g for g in G_elems if get_image(phi, g) in M]
            
        if not preimage_elements:
            neg_q = True
        else:
            # If G is not a group (e.g., just a list/magma), the preimage cannot be a normal subgroup of G
            if not isinstance(G, PermutationGroup):
                neg_q = True
            else:
                preimage_group = PermutationGroup(preimage_elements)
                is_normal = preimage_group.is_subgroup(G) and preimage_group.is_normal(G)
                neg_q = not is_normal
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group",
    "H_2: phi is a group homomorphism from G to H",
    "H_3: M is a normal subgroup of H",
    "¬Q: The preimage phi^{-1}(M) is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3