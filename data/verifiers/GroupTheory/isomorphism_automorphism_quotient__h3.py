import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        N, H, phi, psi = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: N and H are groups
    try:
        h1 = isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    def apply_action(action, h, n):
        if callable(action):
            return action(h, n)
        else:
            return action[h][n]

    # H2: phi is a homomorphism H -> Aut(N)
    try:
        N_elems = list(N.generate())
        H_elems = list(H.generate())
        
        h2 = True
        for h in H_elems:
            for n1 in N_elems:
                for n2 in N_elems:
                    if apply_action(phi, h, n1 * n2) != apply_action(phi, h, n1) * apply_action(phi, h, n2):
                        h2 = False
                        break
                if not h2: break
            if not h2: break
            
        if h2:
            for h1_elem in H_elems:
                for h2_elem in H_elems:
                    for n in N_elems:
                        if apply_action(phi, h1_elem * h2_elem, n) != apply_action(phi, h1_elem, apply_action(phi, h2_elem, n)):
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
                
        if h2:
            for h in H_elems:
                img = set(apply_action(phi, h, n) for n in N_elems)
                if len(img) != len(N_elems):
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # H3: psi is a homomorphism H -> Aut(N)
    try:
        h3 = True
        for h in H_elems:
            for n1 in N_elems:
                for n2 in N_elems:
                    if apply_action(psi, h, n1 * n2) != apply_action(psi, h, n1) * apply_action(psi, h, n2):
                        h3 = False
                        break
                if not h3: break
            if not h3: break
            
        if h3:
            for h1_elem in H_elems:
                for h2_elem in H_elems:
                    for n in N_elems:
                        if apply_action(psi, h1_elem * h2_elem, n) != apply_action(psi, h1_elem, apply_action(psi, h2_elem, n)):
                            h3 = False
                            break
                    if not h3: break
                if not h3: break
                
        if h3:
            for h in H_elems:
                img = set(apply_action(psi, h, n) for n in N_elems)
                if len(img) != len(N_elems):
                    h3 = False
                    break
    except Exception:
        h3 = False
        
    # Negated Conclusion: The semidirect products are NOT isomorphic
    try:
        def build_sdp(N, H, action):
            N_elems = list(N.generate())
            H_elems = list(H.generate())
            sdp_elems = [(n, h) for n in N_elems for h in H_elems]
            elem_to_idx = {elem: i for i, elem in enumerate(sdp_elems)}
            
            perms = []
            for g in sdp_elems:
                g_n, g_h = g
                perm_array = []
                for x in sdp_elems:
                    x_n, x_h = x
                    res_n = g_n * apply_action(action, g_h, x_n)
                    res_h = g_h * x_h
                    perm_array.append(elem_to_idx[(res_n, res_h)])
                perms.append(Permutation(perm_array))
                
            return PermutationGroup(perms)
            
        G_phi = build_sdp(N, H, phi)
        G_psi = build_sdp(N, H, psi)
        
        def are_isomorphic(G1, G2):
            if G1.order() != G2.order():
                return False
            if G1.is_abelian != G2.is_abelian:
                return False
            
            profile1 = sorted([g.order() for g in G1.generate()])
            profile2 = sorted([g.order() for g in G2.generate()])
            if profile1 != profile2:
                return False
                
            try:
                return G1.is_isomorphic(G2)
            except Exception:
                # Fallback if is_isomorphic is not implemented or fails
                return True
                
        neg_q = not are_isomorphic(G_phi, G_psi)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a homomorphism from H to Aut(N)",
    "H_3: psi is a homomorphism from H to Aut(N)",
    "¬Q: The semidirect products N ⋊_phi H and N ⋊_psi H are not isomorphic"
]

N_HYP = 3
NEG_Q_INDEX = 3