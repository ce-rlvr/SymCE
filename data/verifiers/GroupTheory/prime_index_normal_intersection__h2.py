import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            H = witness.get('H')
            p = witness.get('p')
        else:
            G, N, H, p = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H_3: index of N in G is p
    try:
        if isinstance(N, PermutationGroup) and N.is_subgroup(G):
            h3 = (G.order() == p * N.order())
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: H is a subgroup of G
    try:
        h4 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h4 = False

    # neg_Q: H is not a subset of N and index of H cap N in H is not p
    try:
        elements_H = set(H.generate())
        elements_N = set(N.generate())
        intersection_elements = elements_H.intersection(elements_N)
        
        is_subset = elements_H.issubset(elements_N)
        index = len(elements_H) // len(intersection_elements)
        
        neg_q = (not is_subset) and (index != p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: p is a prime number", "H_3: index of N in G is p", "H_4: H is a subgroup of G", "¬Q: H is not a subset of N and index of H cap N in H is not p"]

N_HYP = 4
NEG_Q_INDEX = 4