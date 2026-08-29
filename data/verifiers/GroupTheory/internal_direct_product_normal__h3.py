import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
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

def is_in_group(g, G):
    try:
        degree = G.degree
        if g.size > degree:
            for i in range(degree, g.size):
                if g(i) != i:
                    return False
        p = [g(i) for i in range(degree)]
        g_pad = Permutation(p)
        return g_pad in G
    except Exception:
        return False

def get_normalized_elements(H, degree):
    elems = set()
    for h in H.generate():
        p = [h(i) for i in range(degree)]
        elems.add(Permutation(p))
    return elems

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False] * 5
        G, N, M = witness
    except Exception:
        return [False] * 5

    # H1: G is a group, N and M are subgroups of G
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              isinstance(M, PermutationGroup) and
              all(is_in_group(g, G) for g in N.generators) and
              all(is_in_group(g, G) for g in M.generators))
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if h1:
            degree = G.degree
            N_elems = get_normalized_elements(N, degree)
            
            h2 = True
            for g in G.generators:
                g_norm = Permutation([g(i) for i in range(degree)])
                g_inv = ~g_norm
                for n in N.generators:
                    n_norm = Permutation([n(i) for i in range(degree)])
                    conj = g_norm * n_norm * g_inv
                    if conj not in N_elems:
                        h2 = False
                        break
                if not h2:
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: G = NM
    try:
        if h1:
            degree = G.degree
            N_elems = get_normalized_elements(N, degree)
            M_elems = get_normalized_elements(M, degree)
            
            NM_set = set(n * m for n in N_elems for m in M_elems)
            h3 = (len(NM_set) == G.order())
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: N \cap M = {e}
    try:
        if h1:
            degree = G.degree
            N_elems = get_normalized_elements(N, degree)
            M_elems = get_normalized_elements(M, degree)
            
            intersection = N_elems.intersection(M_elems)
            h4 = (len(intersection) == 1)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: G is NOT isomorphic to N \times M
    try:
        if h1:
            degN = max(N.degree, 1)
            degM = max(M.degree, 1)
            gens = []
            for g in N.generators:
                p = [g(i) if i < degN else i for i in range(degN + degM)]
                gens.append(Permutation(p))
            for h in M.generators:
                p = [i if i < degN else h(i - degN) + degN for i in range(degN + degM)]
                gens.append(Permutation(p))
            if not gens:
                NxM = PermutationGroup([Permutation(0)])
            else:
                NxM = PermutationGroup(gens)
            
            if G.order() != NxM.order():
                neg_q = True
            else:
                neg_q = not G.is_isomorphic(NxM)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group, N and M are subgroups of G",
    "H_2: N is a normal subgroup of G",
    "H_3: G = NM",
    "H_4: N \\cap M = {e}",
    "¬Q: G is not isomorphic to N \\times M"
]

N_HYP = 4
NEG_Q_INDEX = 4