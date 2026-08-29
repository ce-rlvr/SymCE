import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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
trivial = PermutationGroup([Permutation()])

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G, N, H are permutation groups, and N, H are subgroups of G
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              isinstance(H, PermutationGroup) and 
              N.is_subgroup(G) and 
              H.is_subgroup(G))
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = h1 and N.is_normal(G)
    except Exception:
        h2 = False

    # H_3: G is the internal semidirect product of N and H
    try:
        if h1 and h2:
            n_elements = list(N.generate())
            h_elements = list(H.generate())
            h_elements_set = set(h_elements)
            
            # N intersect H is trivial
            int_size = sum(1 for x in n_elements if x in h_elements_set)
            
            # |N| * |H| == |G|
            h3 = (int_size == 1) and (N.order() * H.order() == G.order())
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: H^G is NOT the internal semidirect product of [N, H] and H
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            g_elements = list(G.generate())
            id_perm = g_elements[0]**0
            
            # Compute H^G (normal closure of H in G)
            hg_gens = []
            for g in g_elements:
                g_inv = ~g
                for h in H.generators:
                    hg_gens.append(g * h * g_inv)
            
            if hg_gens:
                H_G = PermutationGroup(hg_gens)
            else:
                H_G = PermutationGroup([id_perm])

            # Compute [N, H] (mixed commutator subgroup)
            comm_gens = []
            for n in n_elements:
                n_inv = ~n
                for h in h_elements:
                    h_inv = ~h
                    comm_gens.append(n * h * n_inv * h_inv)
            
            if comm_gens:
                comm_NH = PermutationGroup(comm_gens)
            else:
                comm_NH = PermutationGroup([id_perm])

            # Check if H_G is the internal semidirect product of comm_NH and H
            # 1. H and comm_NH are subgroups of H_G, and comm_NH is normal in H_G
            cond0 = H.is_subgroup(H_G)
            cond1 = comm_NH.is_subgroup(H_G) and comm_NH.is_normal(H_G)
            
            # 2. comm_NH intersect H is trivial
            comm_elements = list(comm_NH.generate())
            int_comm_H_size = sum(1 for x in comm_elements if x in h_elements_set)
            cond2 = (int_comm_H_size == 1)
            
            # 3. comm_NH * H = H_G
            cond3 = (comm_NH.order() * H.order() == H_G.order())

            # The conclusion holds if all conditions for internal semidirect product are met
            q = cond0 and cond1 and cond2 and cond3
            
            # We want the negation of the conclusion
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G, N, H are permutation groups, and N, H are subgroups of G",
    "H_2: N is a normal subgroup of G",
    "H_3: G is the internal semidirect product of N and H",
    "¬Q: H^G is not the internal semidirect product of the mixed commutator subgroup and H"
]

N_HYP = 3
NEG_Q_INDEX = 3