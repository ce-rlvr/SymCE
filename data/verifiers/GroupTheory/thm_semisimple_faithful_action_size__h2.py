import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conditions(witness):
    G = witness
    is_hom = False
    
    # Handle different possible representations of the action
    if type(witness).__name__ == 'Homomorphism':
        G = witness.domain
        is_hom = True
    elif isinstance(witness, tuple) and len(witness) >= 1:
        G = witness[0]

    # H1: G is a non-trivial finite semisimple group
    # A finite group is semisimple if it has no non-trivial abelian normal subgroups.
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            if G.order() > 1:
                h1 = True
                for N in G.normal_subgroups():
                    if N.order() > 1 and N.is_abelian:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: G acts on the set X
    try:
        if is_hom:
            h2 = isinstance(witness.codomain, PermutationGroup)
        else:
            # A PermutationGroup naturally acts on its domain
            h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    # neg_Q: The action of G on X is faithful
    try:
        if is_hom:
            neg_q = witness.kernel().order() == 1
        else:
            # A PermutationGroup's natural action on its domain is faithful by definition
            neg_q = isinstance(G, PermutationGroup)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a non-trivial finite semisimple group",
    "H_2: G acts on the set X",
    "¬Q: The action of G on X is faithful"
]

N_HYP = 2
NEG_Q_INDEX = 2