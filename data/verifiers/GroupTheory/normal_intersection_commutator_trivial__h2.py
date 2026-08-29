import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    Given a witness (G, N), checks if it is a valid counterexample to the false conjecture:
    Hypotheses:
      - G is a group and N is a subgroup of G
      - N \cap G' is the trivial subgroup
    Conclusion:
      - N is contained in the center Z(G)
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group and N is a subgroup of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
        if h1:
            # Check if all generators of N are in G
            for gen in N.generators:
                if gen not in G:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: The intersection N \cap G' is the trivial subgroup
    try:
        if not h1:
            h2 = False
        else:
            G_prime = G.derived_subgroup()
            h2 = True
            elements = N.elements if hasattr(N, 'elements') else list(N.generate())
            for g in elements:
                if g in G_prime and not g.is_Identity:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: N is not contained in the center Z(G)
    # This means there exists some n in N and g in G that do not commute.
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = False
            for n in N.generators:
                for g in G.generators:
                    if n * g != g * n:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "H_2: The intersection N \\cap G' is the trivial subgroup",
    "¬Q: N is not contained in the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2