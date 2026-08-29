import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
import math
import itertools
import functools

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample.
    The witness is expected to be a tuple: (Gamma, H, G, G_prime)
    where:
      - Gamma: The Galois group of the normal closure E/K.
      - H: The subgroup of Gamma corresponding to the intermediate field L.
      - G: The automorphism group Aut(L/K).
      - G_prime: The commutator subgroup of G.
    """
    try:
        if len(witness) != 4:
            return [False, False]
        Gamma, H, G, G_prime = witness
    except Exception:
        return [False, False]

    # H_1: G' is the commutator subgroup of G
    try:
        h1 = bool(G_prime == G.derived_subgroup())
    except Exception:
        h1 = False

    # neg_Q: The fixed field L^{G'} is NOT the maximal abelian extension of K contained in L
    try:
        if not isinstance(Gamma, PermutationGroup) or not isinstance(H, PermutationGroup):
            neg_q = False
        elif Gamma.order() > 1000:
            neg_q = False
        elif not H.is_subgroup(Gamma):
            neg_q = False
        else:
            # Under the Galois correspondence:
            # L corresponds to H.
            # K corresponds to Gamma.
            # Aut(L/K) corresponds to N_Gamma(H) / H.
            
            # Compute the normalizer N = N_Gamma(H)
            h_gens = H.generators if H.generators else [H.identity]
            norm_gens = []
            for g in Gamma.elements:
                if all((g * h * ~g) in H for h in h_gens):
                    norm_gens.append(g)
            
            if not norm_gens:
                norm_gens = [Gamma.identity]
            N = PermutationGroup(norm_gens)
            
            # The commutator subgroup of Aut(L/K) corresponds to N' H / H.
            # The fixed field L^{G'} corresponds to the preimage of this subgroup in N,
            # which is exactly H^* = <H, N'>.
            N_prime = N.derived_subgroup()
            H_star_gens = list(H.generators) + list(N_prime.generators)
            if not H_star_gens:
                H_star_gens = [Gamma.identity]
            H_star = PermutationGroup(H_star_gens)
            
            # The maximal abelian extension of K contained in L corresponds to the 
            # smallest normal subgroup of Gamma containing H such that the quotient is abelian.
            # This is exactly A = <H, Gamma'>.
            Gamma_prime = Gamma.derived_subgroup()
            A_gens = list(H.generators) + list(Gamma_prime.generators)
            if not A_gens:
                A_gens = [Gamma.identity]
            A = PermutationGroup(A_gens)
            
            # The conclusion holds if L^{G'} is the maximal abelian extension, i.e., H^* == A.
            # We want the conclusion to FAIL.
            neg_q = bool(H_star != A)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G' is the commutator subgroup of G",
    "¬Q: The fixed field L^{G'} is not the maximal abelian extension of K contained in L"
]

N_HYP = 1
NEG_Q_INDEX = 1