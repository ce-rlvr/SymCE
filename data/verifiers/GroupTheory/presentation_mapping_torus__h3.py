import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def evaluate_word(word, S, identity):
    res = identity
    for idx, power in word:
        if power >= 0:
            for _ in range(power):
                res = res * S[idx]
        else:
            inv = S[idx]**-1
            for _ in range(-power):
                res = res * inv
    return res

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (H, S, R, phi_map, G)
    where:
      - H is a PermutationGroup
      - S is a list of generators (Permutation objects in H)
      - R is a list of relations, each represented as a list of (generator_index, power) tuples
      - phi_map is a list of Permutation objects representing the images of S under the automorphism phi
      - G is a PermutationGroup to test against the mapping torus presentation
    """
    try:
        if len(witness) != 5:
            return [False, False, False]
        H, S, R, phi_map, G = witness
    except Exception:
        return [False, False, False]
        
    # H_1: H is a group with presentation <S | R>
    try:
        h1 = False
        if isinstance(H, PermutationGroup):
            s_in_H = all(s in H for s in S)
            if s_in_H:
                gen_order = 1 if not S else PermutationGroup(S).order()
                if gen_order == H.order():
                    r_valid = True
                    for word in R:
                        if evaluate_word(word, S, H.identity) != H.identity:
                            r_valid = False
                            break
                    if r_valid:
                        # Verify it's a known exact presentation to ensure H is not just a proper quotient
                        if len(S) == 0 and len(R) == 0 and H.order() == 1:
                            h1 = True
                        elif len(S) == 1 and len(R) == 1:
                            power = sum(p for idx, p in R[0] if idx == 0)
                            if abs(power) == H.order():
                                h1 = True
                        elif len(S) == 2 and len(R) == 3:
                            if H.order() == 4:
                                h1 = True
                        elif len(S) == 2 and len(R) == 2:
                            if H.order() == 6:
                                h1 = True
    except Exception:
        h1 = False
        
    # H_2: phi is an automorphism of H
    try:
        h2 = False
        if isinstance(H, PermutationGroup) and len(phi_map) == len(S):
            phi_in_H = all(p in H for p in phi_map)
            if phi_in_H:
                gen_order = 1 if not phi_map else PermutationGroup(phi_map).order()
                # Since H is finite, a surjective homomorphism H -> H is an automorphism
                if gen_order == H.order():
                    r_valid = True
                    for word in R:
                        if evaluate_word(word, phi_map, H.identity) != H.identity:
                            r_valid = False
                            break
                    if r_valid:
                        h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: G does not admit the presentation <S, t | R, t s t^-1 = phi(s)>
    try:
        neg_q = False
        # The presentation defines the mapping torus H \rtimes_\phi Z.
        # Since H is a finite group, its mapping torus maps homomorphically onto Z, hence is infinite.
        # If G is a PermutationGroup, it is finite, so it cannot be isomorphic to the mapping torus.
        if isinstance(G, PermutationGroup):
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group with presentation <S | R>",
    "H_2: phi is an automorphism of H",
    "not Q: G does not admit the presentation <S, t | R, t s t^-1 = phi(s) for all s in S>"
]

N_HYP = 2
NEG_Q_INDEX = 2