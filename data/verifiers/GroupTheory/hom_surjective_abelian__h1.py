import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]
    
    # H_1: phi is a surjective group homomorphism from G to H
    h1_ok = False
    try:
        if hasattr(G, 'elements') and hasattr(H, 'elements'):
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            
            if isinstance(phi, dict):
                phi_func = lambda x: phi[x]
            elif isinstance(phi, (list, tuple, set)):
                phi_dict = dict(phi)
                phi_func = lambda x: phi_dict[x]
            else:
                phi_func = phi
                
            valid_map = True
            for g in G_elems:
                try:
                    val = phi_func(g)
                    if val not in H_elems:
                        valid_map = False
                        break
                except Exception:
                    valid_map = False
                    break
            
            if valid_map:
                is_hom = True
                for g1 in G_elems:
                    for g2 in G_elems:
                        if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                            is_hom = False
                            break
                    if not is_hom:
                        break
                
                if is_hom:
                    image = []
                    for g in G_elems:
                        val = phi_func(g)
                        if val not in image:
                            image.append(val)
                    if len(image) == len(H_elems):
                        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: G is an abelian group
    h2_ok = False
    try:
        h2_ok = bool(G.is_abelian)
    except Exception:
        h2_ok = False

    # neg_Q: H is not an abelian group
    neg_q_ok = False
    try:
        neg_q_ok = not bool(H.is_abelian)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is a surjective group homomorphism from G to H",
    "H_2: G is an abelian group",
    "¬Q: H is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2