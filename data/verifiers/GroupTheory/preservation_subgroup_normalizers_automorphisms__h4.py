import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: phi is an automorphism of G",
    "¬Q: N_G(phi(H)) != phi(N_G(H))"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of G
    try:
        if not h1:
            h2 = False
        else:
            if isinstance(H, PermutationGroup):
                H_elements = set(H.generate())
            else:
                H_elements = set(H)
                
            G_elements_set = set(G.generate())
            
            if not H_elements or not H_elements.issubset(G_elements_set):
                h2 = False
            else:
                h2 = True
                for h_a in H_elements:
                    if h_a**-1 not in H_elements:
                        h2 = False
                        break
                    for h_b in H_elements:
                        if h_a * h_b not in H_elements:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # H3: phi is an automorphism of G
    try:
        if not h1:
            h3 = False
        else:
            G_elements = list(G.generate())
            G_elements_set = set(G_elements)
            
            if isinstance(phi, dict):
                phi_func = lambda x: phi[x]
            elif isinstance(phi, Permutation):
                phi_func = lambda x: phi * x * phi**-1
            else:
                phi_func = phi
                
            images = []
            h3 = True
            for g in G_elements:
                img = phi_func(g)
                if img not in G_elements_set:
                    h3 = False
                    break
                images.append(img)
                
            if h3:
                if len(set(images)) != len(G_elements):
                    h3 = False
                else:
                    for g1 in G_elements:
                        for g2 in G_elements:
                            if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                                h3 = False
                                break
                        if not h3:
                            break
    except Exception:
        h3 = False
        
    # neg_Q: N_G(phi(H)) != phi(N_G(H))
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            G_elements = list(G.generate())
            if isinstance(H, PermutationGroup):
                H_elements = set(H.generate())
            else:
                H_elements = set(H)
            
            if isinstance(phi, dict):
                phi_func = lambda x: phi[x]
            elif isinstance(phi, Permutation):
                phi_func = lambda x: phi * x * phi**-1
            else:
                phi_func = phi
                
            phi_H_elements = {phi_func(h) for h in H_elements}
            
            def normalizes(g, subset):
                g_inv = g ** -1
                for x in subset:
                    if g * x * g_inv not in subset:
                        return False
                return True
                
            N_G_H = {g for g in G_elements if normalizes(g, H_elements)}
            N_G_phi_H = {g for g in G_elements if normalizes(g, phi_H_elements)}
            
            phi_N_G_H = {phi_func(g) for g in N_G_H}
            
            neg_q = N_G_phi_H != phi_N_G_H
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]