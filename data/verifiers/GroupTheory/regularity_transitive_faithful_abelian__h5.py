import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    # Allow witness to be a list of permutations generating the group
    try:
        if isinstance(witness, list):
            witness = PermutationGroup(witness)
    except Exception:
        pass

    # H1: G is an abelian group
    try:
        h1 = bool(witness.is_abelian)
    except Exception:
        h1 = False

    # H2: X is a non-empty set
    try:
        h2 = bool(witness.degree > 0)
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        # A PermutationGroup inherently acts on the set {0, 1, ..., degree-1}
        h3 = isinstance(witness, PermutationGroup)
    except Exception:
        h3 = False

    # H4: The action of G on X is faithful
    try:
        # The action of a PermutationGroup on its domain is always faithful
        h4 = isinstance(witness, PermutationGroup)
    except Exception:
        h4 = False

    # neg_Q: The stabilizer of some point in X is not the trivial subgroup
    try:
        neg_q = False
        if isinstance(witness, PermutationGroup) and witness.degree > 0:
            for i in range(witness.degree):
                stab = witness.stabilizer(i)
                
                trivial_stab = False
                if hasattr(stab, 'is_trivial') and stab.is_trivial is not None:
                    trivial_stab = bool(stab.is_trivial)
                else:
                    try:
                        ord_val = stab.order() if callable(stab.order) else stab.order
                        trivial_stab = (ord_val == 1)
                    except Exception:
                        trivial_stab = all(gen.is_Identity for gen in stab.generators)
                
                if not trivial_stab:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: X is a non-empty set",
    "H_3: G acts on X",
    "H_4: The action of G on X is faithful",
    "¬Q: The stabilizer of some point in X is not the trivial subgroup"
]

N_HYP = 4
NEG_Q_INDEX = 4