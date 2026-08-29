import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    try:
        if len(witness) == 3:
            G, phi1, phi2 = witness
        elif len(witness) == 5:
            G, H1, H2, phi1, phi2 = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def check_hom_and_ker(phi, G):
        from sympy.combinatorics.homomorphisms import GroupHomomorphism
        if isinstance(phi, GroupHomomorphism):
            if phi.domain != G:
                return False, set()
            return True, set(phi.kernel().elements)
        elif callable(phi):
            try:
                elements = list(G.elements)
                id_img = phi(G.identity)
                ker = set()
                for g1 in elements:
                    if phi(g1) == id_img:
                        ker.add(g1)
                    for g2 in elements:
                        if phi(g1 * g2) != phi(g1) * phi(g2):
                            return False, set()
                return True, ker
            except Exception:
                return False, set()
        elif isinstance(phi, dict):
            try:
                elements = list(G.elements)
                id_img = phi[G.identity]
                ker = set()
                for g1 in elements:
                    if phi[g1] == id_img:
                        ker.add(g1)
                    for g2 in elements:
                        if phi[g1 * g2] != phi[g1] * phi[g2]:
                            return False, set()
                return True, ker
            except Exception:
                return False, set()
        return False, set()

    # H_1: phi1 is a group homomorphism from G
    try:
        h1, ker1_elements = check_hom_and_ker(phi1, G)
    except Exception:
        h1 = False

    # H_2: phi2 is a group homomorphism from G
    try:
        h2, ker2_elements = check_hom_and_ker(phi2, G)
    except Exception:
        h2 = False

    # neg_Q: ker(phi1) \cap ker(phi2) is NOT a normal subgroup of G
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            intersection_elements = ker1_elements.intersection(ker2_elements)
            
            is_normal = True
            for g in G.generators:
                g_inv = g**-1
                for k in intersection_elements:
                    if g * k * g_inv not in intersection_elements:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi1 is a group homomorphism from G",
    "H_2: phi2 is a group homomorphism from G",
    "¬Q: ker(phi1) intersection ker(phi2) is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2