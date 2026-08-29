import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def apply_phi(phi, g):
    if isinstance(phi, dict):
        return phi[g]
    else:
        return phi(g)

def is_group(G):
    return hasattr(G, 'elements') and hasattr(G, 'generators')

def is_homomorphism(G, H, phi):
    try:
        H_elems = set(H.elements)
        for g in G.elements:
            if apply_phi(phi, g) not in H_elems:
                return False
        for g1 in G.elements:
            for g2 in G.elements:
                p1 = apply_phi(phi, g1)
                p2 = apply_phi(phi, g2)
                p12 = apply_phi(phi, g1 * g2)
                if p1 * p2 != p12:
                    return False
        return True
    except Exception:
        return False

def get_all_subgroups(G):
    elements = list(G.elements)
    subgroups_sets = set()
    subgroups = []
    subgroups_sets_list = []
    
    for g in elements:
        H = PermutationGroup([g])
        H_set = frozenset(H.elements)
        if H_set not in subgroups_sets:
            subgroups_sets.add(H_set)
            subgroups.append(H)
            subgroups_sets_list.append(H_set)
            
    head = 0
    while head < len(subgroups):
        for i in range(head):
            H1_set = subgroups_sets_list[i]
            H2_set = subgroups_sets_list[head]
            if H1_set.issubset(H2_set) or H2_set.issubset(H1_set):
                continue
            gens = subgroups[i].generators + subgroups[head].generators
            K = PermutationGroup(gens)
            K_set = frozenset(K.elements)
            if K_set not in subgroups_sets:
                subgroups_sets.add(K_set)
                subgroups.append(K)
                subgroups_sets_list.append(K_set)
        head += 1
        
    return subgroups, subgroups_sets_list

def get_frattini_subgroup(G):
    elements = list(G.elements)
    if len(elements) == 1:
        return set(elements)
    subgroups, subgroups_sets_list = get_all_subgroups(G)
    G_set = frozenset(elements)
    
    maximal_subgroups = []
    for i, M_set in enumerate(subgroups_sets_list):
        if M_set == G_set:
            continue
        is_maximal = True
        for j, K_set in enumerate(subgroups_sets_list):
            if K_set == G_set or K_set == M_set:
                continue
            if M_set.issubset(K_set):
                is_maximal = False
                break
        if is_maximal:
            maximal_subgroups.append(M_set)
            
    if not maximal_subgroups:
        return set(G_set)
        
    frattini_set = set(G_set)
    for M_set in maximal_subgroups:
        frattini_set = frattini_set.intersection(M_set)
        
    return frattini_set

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
        phi = witness.get('phi')
        Phi_G = witness.get('Phi_G', None)
        Phi_H = witness.get('Phi_H', None)
    elif isinstance(witness, (list, tuple)):
        G = witness[0] if len(witness) > 0 else None
        H = witness[1] if len(witness) > 1 else None
        phi = witness[2] if len(witness) > 2 else None
        Phi_G = witness[3] if len(witness) > 3 else None
        Phi_H = witness[4] if len(witness) > 4 else None
    else:
        G = getattr(witness, 'G', None)
        H = getattr(witness, 'H', None)
        phi = getattr(witness, 'phi', None)
        Phi_G = getattr(witness, 'Phi_G', None)
        Phi_H = getattr(witness, 'Phi_H', None)

    h1_ok = False
    try:
        if is_group(G) and is_group(H) and is_homomorphism(G, H, phi):
            h1_ok = True
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if h1_ok:
            actual_Phi_G = get_frattini_subgroup(G)
            actual_Phi_H = get_frattini_subgroup(H)
            
            if Phi_G is not None:
                if hasattr(Phi_G, 'elements'):
                    set_Phi_G = set(Phi_G.elements)
                else:
                    set_Phi_G = set(Phi_G)
                if set_Phi_G != actual_Phi_G:
                    h2_ok = False
                else:
                    h2_ok = True
            else:
                Phi_G = actual_Phi_G
                h2_ok = True
                
            if Phi_H is not None:
                if hasattr(Phi_H, 'elements'):
                    set_Phi_H = set(Phi_H.elements)
                else:
                    set_Phi_H = set(Phi_H)
                if set_Phi_H != actual_Phi_H:
                    h2_ok = False
            else:
                Phi_H = actual_Phi_H
                if h2_ok:
                    h2_ok = True
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            if hasattr(Phi_G, 'elements'):
                elements_G = Phi_G.elements
            else:
                elements_G = Phi_G
                
            if hasattr(Phi_H, 'elements'):
                elements_H = set(Phi_H.elements)
            else:
                elements_H = set(Phi_H)
                
            is_subset = True
            for g in elements_G:
                if apply_phi(phi, g) not in elements_H:
                    is_subset = False
                    break
            neg_q_ok = not is_subset
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: \Phi(G) and \Phi(H) denote the Frattini subgroups of G and H",
    "¬Q: \phi(\Phi(G)) is not contained in \Phi(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2