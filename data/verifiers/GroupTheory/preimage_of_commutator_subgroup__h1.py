import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def _extract(witness):
    if isinstance(witness, dict):
        return witness['G'], witness['H'], witness['phi']
    else:
        return witness[0], witness[1], witness[2]

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = _extract(witness)
        
        if callable(phi):
            phi_dict = {g: phi(g) for g in G.elements}
        else:
            phi_dict = phi
            
        h1 = True
        if not hasattr(G, 'elements') or not hasattr(H, 'elements'):
            h1 = False
        else:
            for g in G.elements:
                if g not in phi_dict:
                    h1 = False
                    break
                if phi_dict[g] not in H.elements:
                    h1 = False
                    break
            if h1:
                for x in G.elements:
                    for y in G.elements:
                        if phi_dict[x * y] != phi_dict[x] * phi_dict[y]:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    try:
        G, H, phi = _extract(witness)
        h2 = hasattr(G, 'derived_subgroup') and hasattr(H, 'derived_subgroup')
        if h2:
            _ = G.derived_subgroup()
            _ = H.derived_subgroup()
    except Exception:
        h2 = False

    try:
        G, H, phi = _extract(witness)
        
        if callable(phi):
            phi_dict = {g: phi(g) for g in G.elements}
        else:
            phi_dict = phi
            
        G_comm = G.derived_subgroup()
        H_comm = H.derived_subgroup()
        H_comm_elements = set(H_comm.elements)
        
        preimage = set()
        for g in G.elements:
            if phi_dict[g] in H_comm_elements:
                preimage.add(g)
                
        is_subgroup = True
        id_G = G.identity
        if id_G not in preimage:
            is_subgroup = False
        else:
            for x in preimage:
                if x**-1 not in preimage:
                    is_subgroup = False
                    break
                for y in preimage:
                    if x * y not in preimage:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        is_normal = True
        if is_subgroup:
            for n in preimage:
                for g in G.elements:
                    if g * n * g**-1 not in preimage:
                        is_normal = False
                        break
                if not is_normal:
                    break
        else:
            is_normal = False
            
        contains_G_comm = True
        for x in G_comm.elements:
            if x not in preimage:
                contains_G_comm = False
                break
                
        neg_Q = not (is_normal and contains_G_comm)
    except Exception:
        neg_Q = False

    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: G_comm and H_comm denote the commutator subgroups of G and H",
    "¬Q: the preimage of H_comm is not a normal subgroup of G or does not contain G_comm"
]

N_HYP = 2
NEG_Q_INDEX = 2