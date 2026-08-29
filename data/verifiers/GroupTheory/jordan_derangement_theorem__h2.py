import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Pre-process witness if it's a tuple (G, X) or a list of generators
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, X = witness
            if isinstance(G, PermutationGroup):
                witness = G
                
        if isinstance(witness, list):
            witness = PermutationGroup(witness)
    except Exception:
        pass

    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: |X| >= 2
    try:
        h2 = isinstance(witness, PermutationGroup) and bool(witness.degree >= 2)
    except Exception:
        h2 = False

    # H_3: The action of G on X is transitive
    try:
        h3 = isinstance(witness, PermutationGroup) and bool(witness.is_transitive())
    except Exception:
        h3 = False

    # ¬Q: Every element g in G has at least one fixed point in X
    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            neg_q = True
            for p in witness.generate():
                has_fixed = False
                for i in range(witness.degree):
                    if p(i) == i:
                        has_fixed = True
                        break
                if not has_fixed:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: |X| >= 2",
    "H_3: The action of G on X is transitive",
    "¬Q: Every element g in G has at least one fixed point in X"
]

N_HYP = 3
NEG_Q_INDEX = 3