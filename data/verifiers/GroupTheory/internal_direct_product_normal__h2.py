import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from itertools import product

# Top-level setup for witness expressions
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

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: M is a normal subgroup of G",
    "H_3: G = NM",
    "H_4: The intersection of N and M is the trivial subgroup {e}",
    "¬Q: G is not isomorphic to the direct product N \\times M"
]

def conditions(witness):
    try:
        G, N, M = witness
    except Exception:
        return [False] * 5

    # H1: G is a group (and N, M are subgroups of G)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(M, PermutationGroup)
        if h1:
            h1 = N.is_subgroup(G) and M.is_subgroup(G)
    except Exception:
        h1 = False

    # H2: M is a normal subgroup of G
    try:
        h2 = M.is_normal(G)
    except Exception:
        h2 = False

    # H3: G = NM
    try:
        NM_elements = set()
        for n in list(N.elements):
            for m in list(M.elements):
                NM_elements.add(n * m)
        h3 = (NM_elements == set(G.elements))
    except Exception:
        h3 = False

    # H4: N \cap M = {e}
    try:
        intersection = set(N.elements).intersection(set(M.elements))
        h4 = (len(intersection) == 1 and list(intersection)[0].is_Identity)
    except Exception:
        h4 = False

    # neg_Q: G is NOT isomorphic to N \times M
    try:
        if N.order() == 1:
            NxM = M
        elif M.order() == 1:
            NxM = N
        else:
            degree_N = N.degree
            degree_M = M.degree
            
            shifted_M_gens = []
            for g in M.generators:
                arr = [i for i in range(degree_N)] + [g(i) + degree_N for i in range(degree_M)]
                shifted_M_gens.append(Permutation(arr))
                
            extended_N_gens = []
            for g in N.generators:
                arr = [g(i) for i in range(degree_N)] + [i + degree_N for i in range(degree_M)]
                extended_N_gens.append(Permutation(arr))
                
            NxM = PermutationGroup(extended_N_gens + shifted_M_gens)
            
        is_iso = None
        if hasattr(G, 'is_isomorphic'):
            try:
                is_iso = G.is_isomorphic(NxM)
            except Exception:
                is_iso = None
                
        if is_iso is None:
            # Fallback isomorphism check for small groups
            def group_invariants(grp):
                orders = sorted([g.order() for g in list(grp.elements)])
                try:
                    center_size = grp.center().order()
                except Exception:
                    center_size = len([x for x in list(grp.elements) if all(x * y == y * x for y in list(grp.elements))])
                try:
                    derived_size = grp.derived_subgroup().order()
                except Exception:
                    derived_size = -1
                is_abelian = grp.is_abelian
                return (orders, center_size, derived_size, is_abelian)
            
            is_iso = (group_invariants(G) == group_invariants(NxM))
            
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]