import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

CONDITION_LABELS = [
    "H_1: H is a group",
    "H_2: phi is a surjective group homomorphism from G to H",
    "H_3: N is a normal subgroup of G",
    "¬Q: phi(N) is not a normal subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, H, phi, N = witness
    except Exception:
        return [False, False, False, False]
        
    def eval_phi(g):
        if isinstance(phi, dict):
            for k, v in phi.items():
                if k == g:
                    return v
            raise ValueError("Element not in phi domain")
        else:
            return phi(g)

    # H_1: H is a group
    try:
        h_is_group = hasattr(H, 'generate') or hasattr(H, 'elements')
    except Exception:
        h_is_group = False

    # H_2: \phi is a surjective group homomorphism from G to H
    try:
        if not (hasattr(G, 'generate') or hasattr(G, 'elements')) or not (hasattr(H, 'generate') or hasattr(H, 'elements')):
            phi_is_surj_hom = False
        else:
            G_elements = list(G.generate()) if hasattr(G, 'generate') else list(G.elements)
            H_elements = list(H.generate()) if hasattr(H, 'generate') else list(H.elements)
            
            is_hom = True
            mapped_elements = []
            for g in G_elements:
                hg = eval_phi(g)
                found = False
                for h in H_elements:
                    if hg == h:
                        found = True
                        break
                if not found:
                    is_hom = False
                    break
                mapped_elements.append(hg)
                
            if is_hom:
                for g1 in G_elements:
                    for g2 in G_elements:
                        expected = eval_phi(g1 * g2)
                        actual = eval_phi(g1) * eval_phi(g2)
                        if expected != actual:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                        
            if is_hom:
                for h in H_elements:
                    found = False
                    for m in mapped_elements:
                        if m == h:
                            found = True
                            break
                    if not found:
                        phi_is_surj_hom = False
                        break
                else:
                    phi_is_surj_hom = True
            else:
                phi_is_surj_hom = False
    except Exception:
        phi_is_surj_hom = False

    # H_3: N is a normal subgroup of G
    try:
        if not (hasattr(G, 'generate') or hasattr(G, 'elements')):
            n_is_normal = False
        else:
            if hasattr(N, 'generate'):
                N_elements = list(N.generate())
            elif hasattr(N, 'elements'):
                N_elements = list(N.elements)
            else:
                N_elements = list(N)
                
            G_elements = list(G.generate()) if hasattr(G, 'generate') else list(G.elements)
            
            is_sub = True
            for n in N_elements:
                found = False
                for g in G_elements:
                    if n == g:
                        found = True
                        break
                if not found:
                    is_sub = False
                    break
                    
            if is_sub and len(N_elements) > 0:
                is_subgroup = True
                for n1 in N_elements:
                    inv_n1 = n1**-1
                    found = False
                    for n in N_elements:
                        if inv_n1 == n:
                            found = True
                            break
                    if not found:
                        is_subgroup = False
                        break
                        
                    for n2 in N_elements:
                        prod = n1 * n2
                        found = False
                        for n in N_elements:
                            if prod == n:
                                found = True
                                break
                        if not found:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            else:
                is_subgroup = False
                
            if is_subgroup:
                is_normal = True
                for g in G_elements:
                    for n in N_elements:
                        conj = g * n * g**-1
                        found = False
                        for n2 in N_elements:
                            if conj == n2:
                                found = True
                                break
                        if not found:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                n_is_normal = is_normal
            else:
                n_is_normal = False
    except Exception:
        n_is_normal = False

    # neg_Q: \phi(N) is NOT a normal subgroup of H
    try:
        if not (hasattr(H, 'generate') or hasattr(H, 'elements')):
            neg_q = False
        else:
            if hasattr(N, 'generate'):
                N_elements = list(N.generate())
            elif hasattr(N, 'elements'):
                N_elements = list(N.elements)
            else:
                N_elements = list(N)
                
            phi_N = []
            for n in N_elements:
                pn = eval_phi(n)
                found = False
                for x in phi_N:
                    if x == pn:
                        found = True
                        break
                if not found:
                    phi_N.append(pn)
                    
            H_elements = list(H.generate()) if hasattr(H, 'generate') else list(H.elements)
            
            is_subgroup = True
            if len(phi_N) == 0:
                is_subgroup = False
            else:
                for x in phi_N:
                    inv_x = x**-1
                    found = False
                    for y in phi_N:
                        if inv_x == y:
                            found = True
                            break
                    if not found:
                        is_subgroup = False
                        break
                        
                    for y in phi_N:
                        prod = x * y
                        found = False
                        for z in phi_N:
                            if prod == z:
                                found = True
                                break
                        if not found:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
            if is_subgroup:
                is_normal = True
                for h in H_elements:
                    for x in phi_N:
                        conj = h * x * h**-1
                        found = False
                        for y in phi_N:
                            if conj == y:
                                found = True
                                break
                        if not found:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h_is_group, phi_is_surj_hom, n_is_normal, neg_q]