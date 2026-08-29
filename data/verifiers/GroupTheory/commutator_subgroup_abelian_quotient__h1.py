import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Standard group theory bindings
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

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for the conjecture.
    The witness is expected to be a tuple (G, N) where G and N are PermutationGroups.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1 = True
        # Check if N is a subgroup of G by verifying all generators of N are in G
        for n in N.generators:
            if n not in G:
                h1 = False
                break
        # Check normality: g * n * g^-1 must be in N for all generators g of G and n of N
        if h1:
            for g in G.generators:
                for n in N.generators:
                    if (g * n * g**-1) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: The commutator subgroup derived(G) is a subgroup of N
    try:
        C = G.derived_subgroup()
        h2 = True
        for c in C.generators:
            if c not in N:
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: The quotient group G/N is NOT abelian
    # G/N is abelian iff the commutator of any two elements of G is in N.
    # It suffices to check the commutators of the generators of G.
    try:
        is_abelian = True
        for g1 in G.generators:
            for g2 in G.generators:
                if (g1 * g2 * g1**-1 * g2**-1) not in N:
                    is_abelian = False
                    break
            if not is_abelian:
                break
        neg_q = not is_abelian
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The commutator subgroup derived(G) is a subgroup of N",
    "¬Q: The quotient group G/N is not abelian"
]

N_HYP = 2
NEG_Q_INDEX = 2