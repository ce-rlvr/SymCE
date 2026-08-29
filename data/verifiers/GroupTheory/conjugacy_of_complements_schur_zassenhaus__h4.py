import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
            N = witness.get('N')
            H1 = witness.get('H1')
            H2 = witness.get('H2')
        else:
            G, N, H1, H2 = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False

    try:
        n_is_subgroup = isinstance(N, PermutationGroup) and all(gen in G for gen in N.generators)
        h2 = n_is_subgroup and G.is_normal(N)
    except Exception:
        h2 = False

    try:
        oG = G.order()
        oN = N.order()
        if oG % oN == 0:
            index = oG // oN
            h3 = math.gcd(oN, index) == 1
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        def is_complement(H):
            if not isinstance(H, PermutationGroup):
                return False
            if H.order() * N.order() != G.order():
                return False
            for gen in H.generators:
                if gen not in G:
                    return False
            if math.gcd(H.order(), N.order()) != 1:
                for h in H.generate():
                    if not h.is_Identity and h in N:
                        return False
            return True

        if is_complement(H1) and is_complement(H2):
            are_conjugate = False
            for g in G.generate():
                maps_to_H2 = True
                for h in H1.generators:
                    if (g * h * ~g) not in H2:
                        maps_to_H2 = False
                        break
                if maps_to_H2:
                    are_conjugate = True
                    break
            neg_q = not are_conjugate
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: The order of N and the index of N in G are coprime",
    "¬Q: There exist two complements of N in G that are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3