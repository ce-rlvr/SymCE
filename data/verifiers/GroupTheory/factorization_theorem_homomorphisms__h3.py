import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            phi = witness.get('phi')
            N = witness.get('N')
        else:
            G, H, phi, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: phi is a group homomorphism from G to H
    try:
        h2 = True
        if not h1:
            h2 = False
        else:
            if isinstance(phi, dict):
                def eval_phi(g):
                    return phi[g]
            else:
                eval_phi = phi
                
            for g in G.elements:
                if eval_phi(g) not in H.elements:
                    h2 = False
                    break
            if h2:
                for g1 in G.elements:
                    for g2 in G.elements:
                        if eval_phi(g1 * g2) != eval_phi(g1) * eval_phi(g2):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    try:
        if not h1:
            neg_q = False
        else:
            if isinstance(N, PermutationGroup):
                n_elements = set(N.elements)
            else:
                n_elements = set(N)
                
            is_subgroup = True
            for n in n_elements:
                if n not in G.elements:
                    is_subgroup = False
                    break
            
            if is_subgroup:
                # Find identity of G
                id_G = None
                for g in G.elements:
                    if g * g == g:
                        id_G = g
                        break
                if id_G not in n_elements:
                    is_subgroup = False
                
                # Check closure and inverses
                for n1 in n_elements:
                    if ~n1 not in n_elements:
                        is_subgroup = False
                    for n2 in n_elements:
                        if n1 * n2 not in n_elements:
                            is_subgroup = False
            
            is_normal = False
            if is_subgroup:
                is_normal = True
                for g in G.elements:
                    left_coset = set(g * n for n in n_elements)
                    right_coset = set(n * g for n in n_elements)
                    if left_coset != right_coset:
                        is_normal = False
                        break
                        
            # Find identity of H
            id_H = None
            for h in H.elements:
                if h * h == h:
                    id_H = h
                    break
                    
            is_in_ker = True
            if is_normal:
                if isinstance(phi, dict):
                    def eval_phi_n(g):
                        return phi[g]
                else:
                    eval_phi_n = phi
                for n in n_elements:
                    if eval_phi_n(n) != id_H:
                        is_in_ker = False
                        break
                    
            # The conclusion holds iff N is a normal subgroup and N is a subset of ker(phi)
            conclusion_holds = is_normal and is_in_ker
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "¬Q: N is not a normal subgroup of G or N is not a subset of ker(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2