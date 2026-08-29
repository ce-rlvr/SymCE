import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis was that G is a group (the witness is just a set of permutations).
    """
    try:
        # Parse the witness: can be a tuple (degree, perms) or just an iterable of perms
        if isinstance(witness, tuple) and len(witness) == 2 and type(witness[0]) is int:
            degree, perms = witness
            perms = list(perms)
            if any(isinstance(p, Permutation) and p.size > degree for p in perms):
                return [False, False, False, False]
        else:
            if hasattr(witness, 'elements'):
                perms = list(witness.elements)
            else:
                perms = list(witness)
            degree = max(p.size for p in perms) if perms else 0
            
        if not all(isinstance(p, Permutation) for p in perms):
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    def apply_p(p, i):
        try:
            if i < p.size:
                return p(i)
            return i
        except Exception:
            return i

    # H_1: X is a finite set
    # By definition of our representation, the set X = {0, 1, ..., degree-1} is finite.
    h1 = True

    # H_2: |X| >= 2
    try:
        h2 = bool(degree >= 2)
    except Exception:
        h2 = False

    # H_3: G acts transitively on X
    try:
        h3 = True
        if degree == 0:
            h3 = False
        else:
            for i in range(degree):
                for j in range(degree):
                    if not any(apply_p(p, i) == j for p in perms):
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # neg_Q: Every element in G has at least one fixed point
    # (Negation of: There exists at least one element g in G that is fixed-point-free)
    try:
        neg_q = True
        for p in perms:
            is_fpf = all(apply_p(p, i) != i for i in range(degree))
            if is_fpf:
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a finite set",
    "H_2: |X| >= 2",
    "H_3: G acts transitively on X",
    "¬Q: Every element in G has at least one fixed point"
]

N_HYP = 3
NEG_Q_INDEX = 3