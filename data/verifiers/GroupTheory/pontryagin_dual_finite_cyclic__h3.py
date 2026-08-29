import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: G is a finite cyclic group
    try:
        h1 = bool(witness.is_cyclic) and witness.order() != sympy.oo
    except Exception:
        h1 = False

    # H_2: \mathbb{T} is the circle group, consisting of complex numbers of absolute value 1 under multiplication
    # This is a definitional hypothesis about the domain, which is always true in this context.
    h2 = True

    # ¬Q: \widehat{G} is not isomorphic to G
    try:
        # The Pontryagin dual \widehat{G} of a finite group G is the group of homomorphisms Hom(G, \mathbb{T}).
        # Since \mathbb{T} is abelian, any such homomorphism factors through the abelianization of G.
        # Thus, \widehat{G} is isomorphic to G/[G,G]. 
        # For \widehat{G} to be isomorphic to G (since G is finite), G must be abelian.
        # Therefore, the conclusion "\widehat{G} is isomorphic to G" fails if and only if G is not abelian.
        neg_q = not bool(witness.is_abelian)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: \\mathbb{T} is the circle group, consisting of complex numbers of absolute value 1 under multiplication",
    "¬Q: \\widehat{G} is not isomorphic to G"
]

N_HYP = 2
NEG_Q_INDEX = 2