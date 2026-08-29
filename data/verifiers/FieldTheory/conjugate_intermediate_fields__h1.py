import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math
import itertools
import functools

# Standard group bindings for witness construction
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Witness is expected to be a tuple of PermutationGroups: (G, H, U1, U2)
    representing the Galois correspondence:
      G  <--> F
      H  <--> E
      U1 <--> K_1
      U2 <--> K_2
    where F <= K_1, K_2 <= E translates to G >= U1, U2 >= H.
    """
    try:
        G, H, U1, U2 = witness
    except Exception:
        return [False, False]

    def is_subgroup(sub, supergroup):
        try:
            for g in sub.generators:
                if g not in supergroup:
                    return False
            return True
        except Exception:
            return False

    def get_normalizer(group, sub):
        gens_sub = sub.generators
        n_elements = []
        for g in group.generate():
            is_norm = True
            for h in gens_sub:
                conj = g * h * (~g)
                if conj not in sub:
                    is_norm = False
                    break
            if is_norm:
                n_elements.append(g)
        return PermutationGroup(*n_elements)

    def are_conjugate_in(N, A, B):
        if A.order() != B.order():
            return False
        gens_A = A.generators
        for n in N.generate():
            is_conj = True
            for g in gens_A:
                conj = n * g * (~n)
                if conj not in B:
                    is_conj = False
                    break
            if is_conj:
                return True
        return False

    # H_1: K_1 and K_2 are intermediate fields between F and E
    try:
        h1_ok = is_subgroup(H, U1) and is_subgroup(U1, G) and \
                is_subgroup(H, U2) and is_subgroup(U2, G)
    except Exception:
        h1_ok = False

    # ¬Q: The equivalence between conjugacy of fields and conjugacy of their absolute Galois groups FAILS
    try:
        if not h1_ok:
            neg_q = False
        else:
            # Gal(E/F) corresponds to N_G(H) / H
            N_G_H = get_normalizer(G, H)
            
            # Gal(E/K_1) corresponds to N_{U1}(H) / H
            N_U1_H = get_normalizer(U1, H)
            
            # Gal(E/K_2) corresponds to N_{U2}(H) / H
            N_U2_H = get_normalizer(U2, H)

            # P1: K_1 and K_2 are mapped to each other by some \sigma \in Gal(E/F)
            P1 = are_conjugate_in(N_G_H, U1, U2)
            
            # P2: Gal(E/K_1) and Gal(E/K_2) are conjugate subgroups in Gal(E/F)
            P2 = are_conjugate_in(N_G_H, N_U1_H, N_U2_H)

            # The conclusion is P1 <==> P2. It fails if P1 != P2.
            neg_q = (P1 != P2)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: K_1 and K_2 are intermediate fields between F and E",
    "¬Q: K_1 and K_2 are mapped to each other by Gal(E/F) iff Gal(E/K_1) and Gal(E/K_2) are conjugate in Gal(E/F) is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1