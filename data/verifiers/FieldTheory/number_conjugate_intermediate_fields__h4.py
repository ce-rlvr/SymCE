import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings for witness expressions
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
            H_E = witness.get('H_E')
            H = witness.get('H')
        else:
            G, H_E, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: L/K is a finite Galois extension
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is the Galois group of L/K
    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: E is an intermediate field between K and L
    try:
        h3 = isinstance(H_E, PermutationGroup)
        if h3:
            for g in H_E.generators:
                if not G.contains(g):
                    h3 = False
                    break
    except Exception:
        h3 = False

    # not Q: The number of distinct intermediate fields conjugate to E over K is not equal to [G : N_G(H)]
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            is_subgroup = True
            for g in H.generators:
                if not G.contains(g):
                    is_subgroup = False
                    break
            
            if not is_subgroup:
                neg_q = False
            else:
                def normalizer_order(group, sub):
                    count = 0
                    for g in group.generate():
                        normalizes = True
                        for h in sub.generators:
                            if not sub.contains(g * h * ~g):
                                normalizes = False
                                break
                        if normalizes:
                            count += 1
                    return count

                n_H_E = normalizer_order(G, H_E)
                n_H = normalizer_order(G, H)
                
                # The number of conjugates of E is [G : N_G(H_E)] = |G| / |N_G(H_E)|
                # The conclusion claims it equals [G : N_G(H)] = |G| / |N_G(H)|
                # Thus, the conclusion fails if and only if |N_G(H_E)| != |N_G(H)|
                neg_q = (n_H_E != n_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: G is the Galois group of L/K",
    "H_3: E is an intermediate field between K and L",
    "not Q: The number of distinct intermediate fields conjugate to E over K is not equal to the index of N_G(H) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3