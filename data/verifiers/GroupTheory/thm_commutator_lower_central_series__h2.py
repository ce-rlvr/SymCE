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

def commutator_subgroup(H, K, G):
    """
    Computes the commutator subgroup of H and K where H and K are normal subgroups of G.
    """
    gens_H = H.generators
    gens_K = K.generators
    base_comms = []
    for h in gens_H:
        for k in gens_K:
            base_comms.append((h**-1) * (k**-1) * h * k)
    
    if not base_comms:
        if G.generators:
            id_el = G.generators[0]**-1 * G.generators[0]
        else:
            id_el = Permutation()
        return PermutationGroup([id_el])
        
    closure_gens = list(base_comms)
    G_gens = G.generators
    
    current_group = PermutationGroup(closure_gens)
    
    added = True
    while added:
        added = False
        for g in G_gens:
            for c in list(closure_gens):
                conj = (g**-1) * c * g
                if conj not in current_group:
                    closure_gens.append(conj)
                    current_group = PermutationGroup(closure_gens)
                    added = True
                    
    return current_group

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        G, i, j = witness
        witness_is_tuple = True
    else:
        G = witness
        witness_is_tuple = False

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    h2 = True

    neg_q = False
    try:
        if h1:
            lcs = [None, G]
            
            if witness_is_tuple:
                max_k = i + j
                stabilized = False
                while len(lcs) <= max_k:
                    if stabilized:
                        lcs.append(lcs[-1])
                    else:
                        next_gamma = commutator_subgroup(lcs[-1], G, G)
                        if next_gamma.order() == lcs[-1].order():
                            stabilized = True
                        lcs.append(next_gamma)
                
                def get_gamma(m):
                    if m < len(lcs):
                        return lcs[m]
                    return lcs[-1]

                if i >= 1 and j >= 1:
                    gamma_i = get_gamma(i)
                    gamma_j = get_gamma(j)
                    gamma_ij = get_gamma(i + j)
                    comm = commutator_subgroup(gamma_i, gamma_j, G)
                    
                    is_subgroup = True
                    for gen in comm.generators:
                        if gen not in gamma_ij:
                            is_subgroup = False
                            break
                    neg_q = not is_subgroup
            else:
                while True:
                    next_gamma = commutator_subgroup(lcs[-1], G, G)
                    if next_gamma.order() == lcs[-1].order():
                        break
                    lcs.append(next_gamma)
                
                def get_gamma(m):
                    if m < len(lcs):
                        return lcs[m]
                    return lcs[-1]

                L = len(lcs) - 1
                is_subgroup_all = True
                for i_idx in range(1, L + 2):
                    for j_idx in range(1, L + 2):
                        gamma_i = get_gamma(i_idx)
                        gamma_j = get_gamma(j_idx)
                        gamma_ij = get_gamma(i_idx + j_idx)
                        comm = commutator_subgroup(gamma_i, gamma_j, G)
                        for gen in comm.generators:
                            if gen not in gamma_ij:
                                is_subgroup_all = False
                                break
                        if not is_subgroup_all:
                            break
                    if not is_subgroup_all:
                        break
                neg_q = not is_subgroup_all
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: gamma_k(G) denotes the k-th term of the lower central series of G",
    "not Q: The commutator subgroup of gamma_i(G) and gamma_j(G) is NOT a subgroup of gamma_i+j(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2