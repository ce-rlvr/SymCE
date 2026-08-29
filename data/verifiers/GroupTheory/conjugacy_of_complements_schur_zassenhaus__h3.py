import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                G, N, H1, H2 = witness
            elif len(witness) == 2:
                G, N = witness
                H1, H2 = None, None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        def is_normal_subgroup(G, N):
            if not isinstance(N, PermutationGroup):
                return False
            if not all(G.contains(g) for g in N.generators):
                return False
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(g * n * ~g):
                        return False
            return True
        h2_ok = is_normal_subgroup(G, N)
    except Exception:
        h2_ok = False

    # H_3: Either N or G/N is a solvable group
    try:
        def is_quotient_solvable(G, N):
            D = G
            while True:
                if all(N.contains(g) for g in D.generators):
                    return True
                next_D = D.derived_subgroup()
                if next_D.order() == D.order():
                    break
                D = next_D
            return all(N.contains(g) for g in D.generators)

        if not isinstance(N, PermutationGroup):
            h3_ok = False
        else:
            if N.is_solvable:
                h3_ok = True
            else:
                h3_ok = is_quotient_solvable(G, N)
    except Exception:
        h3_ok = False

    # neg_Q: There exist two complements of N in G that are not conjugate in G
    try:
        def is_complement(G, N, H):
            if not isinstance(H, PermutationGroup):
                return False
            if not all(G.contains(g) for g in H.generators):
                return False
            if H.order() * N.order() != G.order():
                return False
            for h in H.elements:
                if not h.is_Identity and N.contains(h):
                    return False
            return True

        def are_conjugate(G, H1, H2):
            if H1.order() != H2.order():
                return False
            for g in G.elements:
                if all(H2.contains(g * h * ~g) for h in H1.generators):
                    return True
            return False

        def find_complements(G, N):
            K = G.order() // N.order()
            valid_elements = [g for g in G.elements if g.is_Identity or not N.contains(g)]
            complements = []
            max_gens = int(math.log2(K)) + 1 if K > 1 else 1
            
            for r in range(1, max_gens + 1):
                for gens in itertools.combinations(valid_elements, r):
                    try:
                        H = PermutationGroup(list(gens))
                        if H.order() == K:
                            if is_complement(G, N, H):
                                H_elems = set(H.elements)
                                is_new = True
                                for C in complements:
                                    if set(C.elements) == H_elems:
                                        is_new = False
                                        break
                                if is_new:
                                    complements.append(H)
                    except Exception:
                        continue
            return complements

        if len(witness) == 2:
            complements = find_complements(G, N)
            neg_q_ok = False
            for i in range(len(complements)):
                for j in range(i+1, len(complements)):
                    if not are_conjugate(G, complements[i], complements[j]):
                        neg_q_ok = True
                        break
                if neg_q_ok:
                    break
        elif len(witness) == 4:
            if is_complement(G, N, H1) and is_complement(G, N, H2):
                neg_q_ok = not are_conjugate(G, H1, H2)
            else:
                neg_q_ok = False
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: Either N or G/N is a solvable group",
    "¬Q: There exist two complements of N in G that are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3