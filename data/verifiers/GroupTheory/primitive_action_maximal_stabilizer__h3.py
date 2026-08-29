import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
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
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: X is a set containing at least two elements
    try:
        h2 = witness.degree >= 2
    except Exception:
        h2 = False

    # ¬Q: The action of G on X is primitive if and only if the stabilizer of any point x \in X is a maximal subgroup of G (fails)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # P: The action of G on X is primitive
            P = bool(witness.is_primitive())
            
            # Q: The stabilizer of any point x in X is a maximal subgroup of G
            Q = True
            try:
                elements = list(witness.elements)
            except AttributeError:
                elements = list(witness.generate())
                
            for x in range(witness.degree):
                Hx = witness.stabilizer(x)
                
                # A maximal subgroup must be a proper subgroup
                if Hx.order() == witness.order():
                    Q = False
                    break
                
                # Check if Hx is maximal by ensuring no proper subgroup strictly contains it
                is_max = True
                for g in elements:
                    if g not in Hx:
                        gens = list(Hx.generators) + [g]
                        K = PermutationGroup(gens)
                        if K.order() < witness.order():
                            is_max = False
                            break
                if not is_max:
                    Q = False
                    break
            
            # The conclusion is P <-> Q. It fails when P != Q.
            neg_q = (P != Q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set containing at least two elements",
    "¬Q: The action of G on X is primitive iff the stabilizer of any point is maximal (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2