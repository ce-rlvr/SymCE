import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    # H1: G is a finite group
    try:
        G, N = witness
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        G, N = witness
        if not isinstance(N, PermutationGroup):
            h2 = False
        elif not N.is_subgroup(G):
            h2 = False
        else:
            h2 = True
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(~g * n * g):
                        h2 = False
                        break
                    if not N.contains(g * n * ~g):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: G/N is NOT the trivial group AND G/N is NOT isomorphic to a direct product of non-abelian simple groups
    try:
        G, N = witness
        if not (isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)):
            nq = False
        elif G.order() == N.order():
            # G/N is trivial, so the conclusion holds (neg_Q is False)
            nq = False
        else:
            # For finite groups, G/N is a direct product of non-abelian simple groups iff 
            # it is perfect and has no non-trivial abelian normal subgroups.
            
            # 1. Check if G/N is perfect (i.e., G'N = G)
            G_prime = G.derived_subgroup()
            G_prime_N = PermutationGroup(list(G_prime.generators) + list(N.generators))
            
            if G_prime_N.order() != G.order():
                # G/N is not perfect, so it cannot be a direct product of non-abelian simple groups
                nq = True
            else:
                nq = False
                # 2. Check if G/N has a non-trivial abelian normal subgroup
                # This corresponds to a normal subgroup K of G such that K > N and K' <= N
                try:
                    normals = G.normal_subgroups()
                    for K in normals:
                        if K.order() > N.order() and N.is_subgroup(K):
                            K_prime = K.derived_subgroup()
                            if K_prime.is_subgroup(N):
                                nq = True
                                break
                except AttributeError:
                    # Fallback if normal_subgroups() is unavailable: check if G/N has a non-trivial center
                    center_size = 0
                    for g in G.generate():
                        is_central = True
                        for x in G.generators:
                            comm = g * x * (~g) * (~x)
                            if not N.contains(comm):
                                is_central = False
                                break
                        if is_central:
                            center_size += 1
                    if center_size > N.order():
                        nq = True
    except Exception:
        nq = False

    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "¬Q: G/N is neither the trivial group nor isomorphic to a direct product of non-abelian simple groups"
]

N_HYP = 2
NEG_Q_INDEX = 2